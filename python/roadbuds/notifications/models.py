"""Notifications feature module - user notification queue."""

import sqlalchemy

from roadbuds import db


class Notification(db.Base):
    """User notification queue for app alerts and messages.

    Stores notifications for users about assistance requests, offers, reviews, etc.
    """

    __tablename__ = "notifications"
    __table_args__ = {"schema": "roadbuds"}

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.users.id"),
        nullable=False,
    )
    message = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    is_read = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, server_default=sqlalchemy.text("false"))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now())
