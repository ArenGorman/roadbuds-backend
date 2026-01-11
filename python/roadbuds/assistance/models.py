import sqlalchemy
import sqlalchemy.dialects.postgresql as postgresql
from geoalchemy2 import Geometry

from roadbuds import db


REQUEST_STATUS = sqlalchemy.Enum(
    "Active",
    "Taken",
    "Withdrawn",
    "Timeout",
    "Resolved",
    name="request_status",
    schema="roadbuds",
)


class AssistanceType(db.Base):
    __tablename__ = "assistance_types"
    __table_args__ = {"schema": "roadbuds"}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.Text)
    recommendations_url = sqlalchemy.Column(sqlalchemy.String(256))


class AssistanceRequest(db.Base):
    __tablename__ = "assistance_requests"
    __table_args__ = {"schema": "roadbuds"}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    location = sqlalchemy.Column(Geometry("POINT"))
    submitted_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    closing_time = sqlalchemy.Column(sqlalchemy.DateTime)
    description = sqlalchemy.Column(sqlalchemy.Text)
    assistance_type_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.assistance_types.id"),
        nullable=False,
    )
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roadbuds.users.id"))
    status = sqlalchemy.Column(
        REQUEST_STATUS,
        nullable=False,
        server_default=sqlalchemy.text("'Active'::roadbuds.request_status"),
    )


class AssistanceOffer(db.Base):
    __tablename__ = "assistance_offers"
    __table_args__ = {"schema": "roadbuds"}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    request_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.assistance_requests.id"),
        nullable=False,
    )
    helper_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roadbuds.users.id"), nullable=False)
    offered_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    message = sqlalchemy.Column(sqlalchemy.Text)
    location = sqlalchemy.Column(Geometry("POINT"))
