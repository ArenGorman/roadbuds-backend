import pwdlib

password_hash = pwdlib.PasswordHash.recommended()


def get_password_hash(password):
    pw_hash = password_hash.hash(password)
    return pw_hash


def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)
