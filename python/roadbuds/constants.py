import os
import secrets

# secrets.token_hex(16)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRATION_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
