import datetime as dt
import os

import dotenv
import fastapi
import jwt
import jwt.exceptions
import pwdlib
import pydantic
from fastapi import security as fa_security

from roadbuds.users import schemas, models
from roadbuds.db import SessionLocal
from roadbuds import constants, utils


dotenv.load_dotenv()
password_hash = pwdlib.PasswordHash.recommended()
oauth2_scheme = fa_security.OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(
    data: dict, expires_delta: dt.timedelta | None = dt.timedelta(minutes=constants.ACCESS_TOKEN_EXPIRATION_MINUTES)
):
    to_encode = data.copy()
    expire = dt.datetime.now(dt.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constants.JWT_SECRET, algorithm=constants.JWT_ALGORITHM)
    return encoded_jwt


def get_user(session, username: str):
    if username in (user_in_db := session.query(models.User).filter_by(username=username).first()):
        user_dict = user_in_db[username]
        return UserInDB(**user_dict)
    else:
        raise fastapi.HTTPException(404, "User not found")


class UserInDB(schemas.UserBase):
    password_hash: str


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: str
