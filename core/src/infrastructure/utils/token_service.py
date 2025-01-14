import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
access_key = os.getenv("ACCESS_KEY")
refresh_key = os.getenv("REFRESH_KEY")

class TokenService:

    @staticmethod
    async def create_access_token(email_in: str) -> str:
        expire_delta = timedelta(minutes = 5)
        payload = {
            'sub': email_in,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + expire_delta
        }
        token = jwt.encode(payload, access_key, algorithm="HS256")
        return token

    @staticmethod
    async def decode_access_token(token: str) -> Dict[str, str]:
        try:
            payload = jwt.decode(token, access_key, algorithms=["HS256"])
            expire_time = datetime.fromtimestamp(payload['exp']).replace(tzinfo=timezone.utc)
            if expire_time < datetime.now(timezone.utc):
                raise Exception("Token expired")
            
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.DecodeError:
            raise Exception("Invalid token")

    @staticmethod
    async def create_refresh_token(email_in: str) -> str:
        refresh_token_id = uuid.uuid4()
        expire_delta = timedelta(minutes=30)
        payload = {
            'sub': email_in,
            'jti': str(refresh_token_id),
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + expire_delta,
        }
        token = jwt.encode(payload, refresh_key, algorithm="HS256")        
        return token

    @staticmethod
    async def decode_refresh_token(token: str) -> Dict[str, str]:
        try:
            payload = jwt.decode(token, refresh_key, algorithms=["HS256"])
            expire_time = datetime.fromtimestamp(payload['exp']).replace(tzinfo=timezone.utc)
            if expire_time < datetime.now(timezone.utc):
                raise Exception("Token expired")
            
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.DecodeError:
            raise Exception("Invalid token")