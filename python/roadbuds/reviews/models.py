"""Reviews feature module - rating and feedback system."""

import sqlalchemy

from roadbuds import db


class Review(db.Base):
    """Rating and review system for completed assistance requests.

    Users can rate assistance they received or provided (1-5 stars) with optional comments.
    """

    __tablename__ = "reviews"
    __table_args__ = {"schema": "roadbuds"}

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    request_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.assistance_requests.id"),
        nullable=False,
    )
    reviewer_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.users.id"),
        nullable=False,
    )
    rating = sqlalchemy.Column(
        sqlalchemy.SmallInteger,
        nullable=False,
        server_default=sqlalchemy.text("5"),
        comment="Rating from 1 to 5",
    )
    comment = sqlalchemy.Column(sqlalchemy.Text)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now())
