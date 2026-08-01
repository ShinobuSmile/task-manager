import bcrypt


def hash_password(password: str) -> str:
    encoded_password = password.encode("utf-8") # encode the password for bcrypt
    password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return password.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))