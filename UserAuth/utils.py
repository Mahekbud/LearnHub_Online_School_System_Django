import os
from datetime import datetime, timedelta
from jose import JWTError, jwt

from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key') 
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')


def get_token(user_id):
    payload = {
        "user_id": str(user_id), 
        "exp": datetime.utcnow() + timedelta(minutes=30), 
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
                                                       


def decode_token_user_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailed("Invalid token")
        return user_id
    except JWTError:
        raise AuthenticationFailed("Invalid token")