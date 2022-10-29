from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schema


# SECRET_KEY
# Algorithm
# Expriation time

# to get a string like this run:
# openssl rand -hex 32

# Never user your secret key inside the code
SECRET_KEY = "5004136e79532ab2850f6204d1ce2162570f671ee37a8f647309ff4a3c919e75"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)

        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
