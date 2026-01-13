import datetime
import logging

import fastapi
import sqlalchemy
import sqlalchemy.exc

from roadbuds import db, utils
from roadbuds.users import models, schemas

router = fastapi.APIRouter()
session = db.SessionLocal()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/users")
async def create_user(user_schema: schemas.UserCreate):
    # Check for unique field violations
    conflicts = []

    if session.query(models.User).filter_by(email=user_schema.email).first():
        conflicts.append("email")

    if session.query(models.User).filter_by(username=user_schema.username).first():
        conflicts.append("username")

    if conflicts:
        conflict_details = ", ".join([f"{field}='{getattr(user_schema, field)}'" for field in conflicts])
        raise fastapi.HTTPException(
            status_code=409,
            detail={
                "message": "User with these field values already exists",
                "conflicting_fields": conflicts,
                "details": conflict_details,
            },
        )

    # Create new user
    new_user = models.User(
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        username=user_schema.username,
        email=user_schema.email,
        phone=user_schema.phone,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
        password_hash=utils.get_password_hash(user_schema.password),
        photo_url=user_schema.photo_url,
        is_active=True,
    )

    try:
        session.add(new_user)
        session.commit()
        return {
            "message": f'User "{user_schema.username}" created successfully!',
            "user": schemas.UserResponse.model_validate(new_user),
        }
    except sqlalchemy.exc.SQLAlchemyError as e:
        session.rollback()
        log.error(f"Database error during user creation: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Failed to create user")


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = session.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise fastapi.HTTPException(404, "User not found")
    return schemas.UserResponse.model_validate(user)


@router.patch("/users/{user_id}")
async def update_user(user_id: int, user_schema: schemas.UserUpdate):
    """Update a user's fields of a user with ``id=user_id``

    Args:
        user_id: The id of the user to update
        user_schema: The body of the user data

    """
    user = session.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise fastapi.HTTPException(404, "User not found")

    # Get only fields that were explicitly provided in the request
    update_data = user_schema.model_dump(exclude_unset=True)

    if not update_data:
        raise fastapi.HTTPException(400, "No fields provided to update")

    # Prevent ID modification if somehow passed in update_data
    if "id" in update_data:
        raise fastapi.HTTPException(403, "Altering user IDs from API is forbidden")

    # Track updated fields for response
    updated_fields = set()

    # Apply updates
    for field, value in update_data.items():
        if field == "password":
            # Hash password before storing
            user.password_hash = utils.get_password_hash(value)
            log.info(f"Password updated for user {user_id}")
        else:
            # Update other fields directly
            setattr(user, field, value)
        updated_fields.add(field)

    # Update modification timestamp
    user.modified_at = datetime.datetime.now(tz=datetime.timezone.utc)

    session.commit()

    # Return updated user data
    return {
        "message": f"User {user.username} updated successfully",
        "updated_fields": updated_fields,
        "user": schemas.UserResponse.model_validate(user),
    }


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = session.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise fastapi.HTTPException(404, "User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully", "user": schemas.UserResponse.model_validate(user)}
