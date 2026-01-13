import sqlalchemy

from roadbuds import db


CONTACT_TYPE = sqlalchemy.Enum(
    "whatsapp",
    "snapchat",
    "imessage",
    "telegram",
    "viber",
    "phone",
    "sms",
    name="contact_type",
    schema="roadbuds",
)


class User(db.Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "roadbuds"}

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    first_name = sqlalchemy.Column(sqlalchemy.String(64), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(64))
    username = sqlalchemy.Column(sqlalchemy.String(32), nullable=False, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String(120), nullable=False, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now())
    modified_at = sqlalchemy.Column(sqlalchemy.DateTime)
    password_hash = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    photo_url = sqlalchemy.Column(sqlalchemy.String(256))
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    badges = sqlalchemy.Column(
        sqlalchemy.JSON,
        nullable=False,
        server_default=sqlalchemy.text("'{}'::json"),
    )


class UserContactOption(db.Base):
    __tablename__ = "user_contact_options"
    __table_args__ = {"schema": "roadbuds", "comment": "user emergency or trusted contacts"}

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.users.id"),
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    contact_type = sqlalchemy.Column(CONTACT_TYPE, nullable=False, unique=True)
    contact_value = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    is_preferred = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, server_default=sqlalchemy.text("false"))


class Settings(db.Base):
    __tablename__ = "settings"
    __table_args__ = {"schema": "roadbuds", "comment": "user notification settings"}

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("roadbuds.users.id"),
        sqlalchemy.Identity(always=False),
        primary_key=True,
    )
    notify_on_request = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, server_default=sqlalchemy.text("true"))
    notify_on_offer = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, server_default=sqlalchemy.text("true"))
