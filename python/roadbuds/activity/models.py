"""Activity feature module - tracks user activity status."""

import sqlalchemy

from roadbuds import db


class UserActivity(db.Base):
    """Tracks whether users are actively seeking or offering help.

    Maintains current activity status and last action timestamp for timeout detection.
    """

    __tablename__ = "user_activity"
    __table_args__ = {"schema": "roadbuds", "comment": "tracks user activity status if they are looking for help or available to help"}

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.users.id"),
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    user_status = sqlalchemy.Column(
        sqlalchemy.String(32),
        nullable=False,
        server_default=sqlalchemy.text("'Active'"),
    )
    last_action_time = sqlalchemy.Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
    )
