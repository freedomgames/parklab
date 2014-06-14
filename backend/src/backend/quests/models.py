"""SQLAlchemy models for missions."""


import backend
db = backend.db


join_table = db.Table('mission_quests', db.Model.metadata,
    db.Column(
        'mission_id', db.Integer, db.ForeignKey('missions.id'), index=True),
    db.Column('quest_id', db.Integer, db.ForeignKey('quests.id'), index=True),
    db.UniqueConstraint('mission_id', 'quest_id')
)
db.Index('ix_id_combo', join_table.c.mission_id, join_table.c.quest_id)


class Quest(db.Model):
    """Quests are activities within a mission.  Mentors create quests
    and link them to missions.  Learners complete quests.
    """

    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    icon_url = db.Column(db.String, nullable=True)

    user_id = db.Column(
            db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    missions = db.relationship(
            "Mission", secondary=join_table, backref="quests")
