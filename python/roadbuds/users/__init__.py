"""Users feature module - handles user management, authentication, and settings."""

from roadbuds.users.models import CONTACT_TYPE, Settings, User, UserContactOption
from roadbuds.users.router import router
from roadbuds.users.schemas import UserBase, UserCreate, UserResponse, UserUpdate

__all__ = [
    # Models
    "User",
    "UserContactOption",
    "Settings",
    "CONTACT_TYPE",
    # Schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Router
    "router",
]
