"""SQLAlchemy models for users"""


import backend

db = backend.db


class User(db.Model):
    """A user account for either a learner or a mentor."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=True)
    avatar_url = db.Column(db.String, nullable=True)

    view_fields = ['id', 'name', 'organization', 'avatar_url']

    def as_dict(self):
        """Return a serializable dictionary representation of the user."""
        return {field: getattr(self, field) for field in self.view_fields}
