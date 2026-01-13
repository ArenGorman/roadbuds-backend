import datetime
import typing

import pydantic
import pydantic_extra_types.phone_numbers


class UserBase(pydantic.BaseModel):
    first_name: str
    last_name: str
    username: str
    email: pydantic.EmailStr
    phone: pydantic_extra_types.phone_numbers.PhoneNumber
    photo_url: str | None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    first_name: typing.Optional[str | None] = None
    last_name: typing.Optional[str | None] = None
    username: typing.Optional[str | None] = None
    email: typing.Optional[pydantic.EmailStr | None] = None
    phone: typing.Optional[pydantic_extra_types.phone_numbers.PhoneNumber | None] = None
    photo_url: typing.Optional[str | None] = None
    password: typing.Optional[str | None] = None
    updated_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    is_active: typing.Optional[bool | None] = None


class UserResponse(UserBase):
    is_active: bool
    id: int
    user_settings: typing.Optional[dict[str, str] | None] = None
    model_config = pydantic.ConfigDict(from_attributes=True)
