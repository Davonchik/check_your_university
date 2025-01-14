from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password_func(password: str) -> str:
    return pwd_context.hash(password)

def verify_password_func(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)