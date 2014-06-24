"""REST backend for the google analytics UI."""


import flask
import flask_babel
import flask_restful
import flask_sqlalchemy
import flask_user
import logging
import traceback


app = flask.Flask(__name__)
app.config.from_object('backend.config')
api = flask_restful.Api(app)
babel = flask_babel.Babel(app)
db = flask_sqlalchemy.SQLAlchemy(app)

if not app.debug:
    # debug mode defaults to sending errors to stdout/stderr
    # outside debug mode, we still want to print to stdout/stderr
    # because heroku will capture and log that output
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


# We have to import these after defining app, api and db as these
# imports will be looking for those variables.
import backend.common.auth as auth
import backend.missions.views as mission_views
import backend.organizations.views as organization_views
import backend.quests.views as quest_views
import backend.questions.views as question_views
import backend.s3.views as s3_views
import backend.users.models as user_models
import backend.users.views as user_views


db_adapter = flask_user.SQLAlchemyAdapter(db, user_models.User)
flask_user.UserManager(db_adapter, app)


@app.route('/')
def index():
    """Return the index page."""
    return flask.render_template('index.html')


@app.route('/logout')
def logout():
    """Clear the session and return the index page."""
    flask.session.clear()
    return flask.render_template('index.html')


@app.route('/avatar')
@flask_user.login_required
def update_avatar():
    """Example showing how to use s3 for uploading avatar images."""
    user_id = auth.current_user_id()
    user_row = db.session.query(
            user_models.User.name,
            user_models.User.email,
            user_models.User.description,
            user_models.User.avatar_url).filter_by(
                    id=user_id).first()
    if user_row is None:
        # this really should not happen -- the user would have had
        # to have been deleted without killing the session
        return flask.redirect(flask.url_for('login'))
    else:
        return flask.render_template(
                'avatar_example.html',
                user_id=user_id,
                name=user_row[0],
                email=user_row[1],
                description=user_row[2],
                avatar_url=user_row[3],
                user_url=api.url_for(user_views.User, user_id=user_id))


@app.route('/app')
@flask_user.login_required
def app_page():
    """Return the javascript for the app and pass along information
    on the currently logged-in user.
    """
    user_id = auth.current_user_id()
    user_row = db.session.query(
            user_models.User.name, user_models.User.email).filter_by(
                    id=user_id).first()
    if user_row is None:
        # this really should not happen -- the user would have had
        # to have been deleted without killing the session
        return flask.redirect(flask.url_for('login'))
    else:
        return flask.render_template(
                'app.html',
                user_id=user_id,
                user_name=user_row[0],
                user_email=user_row[1],
                user_url=api.url_for(user_views.User, user_id=user_id))


def error_handler(error, status_code=500, payload=None, debug=app.debug):
    """Generic handler to return an exception as a json response."""
    app.logger.exception(error)

    if debug:
        response = {'message': error.message,
                'traceback': traceback.format_exc()}
    else:
        response = {'message': 'server error'}

    if payload is not None:
        response.update(payload)

    response = flask.jsonify(response)
    response.status_code = status_code
    return response

@app.errorhandler(Exception)
def other_error(error):
    """Catch any other exception.
    NOTE:
    This must be the last declared errorhandler or else it will
    swallow up other errorhandlers.
    """
    return error_handler(error, payload={'type': 'general error'})


app.register_blueprint(s3_views.blueprint, url_prefix='/v1')

api.add_resource(user_views.User, '/v1/users/<int:user_id>')

api.add_resource(mission_views.Mission, '/v1/missions/<int:mission_id>')
api.add_resource(mission_views.MissionList, '/v1/missions/')
api.add_resource(
        mission_views.MissionUserList, '/v1/users/<int:user_id>/missions/')

api.add_resource(quest_views.Quest, '/v1/quests/<int:quest_id>')
api.add_resource(quest_views.QuestList, '/v1/quests/')
api.add_resource(quest_views.QuestUserList, '/v1/users/<int:user_id>/quests/')
api.add_resource(
        quest_views.QuestMissionLink,
        '/v1/missions/<int:left_id>/quests/<int:right_id>')
api.add_resource(
        quest_views.QuestMissionLinkList,
        '/v1/missions/<int:mission_id>/quests/')

api.add_resource(
        question_views.Question,
        '/v1/quests/<int:quest_id>/questions/<int:question_id>')
api.add_resource(
        question_views.QuestionList,
        '/v1/quests/<int:parent_id>/questions/')
api.add_resource(
        question_views.QuestionView,
        '/v1/questions/<int:question_id>')

api.add_resource(
        question_views.Answer,
        '/v1/questions/<int:question_id>/answers/<int:answer_id>')
api.add_resource(
        question_views.AnswerList,
        '/v1/questions/<int:parent_id>/answers/')

api.add_resource(
        organization_views.Organization,
        '/v1/organizations/<int:organization_id>')
api.add_resource(organization_views.OrganizationList, '/v1/organizations/')
api.add_resource(
        organization_views.OrganizationUserLink,
        '/v1/organizations/<int:left_id>/users/<int:right_id>')
