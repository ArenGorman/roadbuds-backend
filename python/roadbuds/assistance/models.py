import sqlalchemy
import sqlalchemy.types as types

from roadbuds import db


class PostgreSQLPoint(types.UserDefinedType):
    """Custom type for PostgreSQL POINT geometry type (not PostGIS)."""

    cache_ok = True

    def get_col_spec(self):
        return "POINT"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            # Expect tuple (x, y)
            if isinstance(value, (tuple, list)) and len(value) == 2:
                return f"({value[0]},{value[1]})"
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            # Parse "(x,y)" to tuple
            if isinstance(value, str):
                value = value.strip("()")
                x, y = value.split(",")
                return (float(x), float(y))
            return value
        return process


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

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.Text)
    recommendations_url = sqlalchemy.Column(sqlalchemy.String(256))


class AssistanceRequest(db.Base):
    __tablename__ = "assistance_requests"
    __table_args__ = {"schema": "roadbuds", "comment": "user requests of assistance"}

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    location = sqlalchemy.Column(PostgreSQLPoint)
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
    helper_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roadbuds.users.id"), nullable=False)
    offered_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    message = sqlalchemy.Column(sqlalchemy.Text)
    location = sqlalchemy.Column(PostgreSQLPoint)
