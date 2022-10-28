from jose import JWTError, jwt
from datetime import datetime, timedelta


# SECRET_KEY
# Algorithm
# Expriation time

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "5004136e79532ab2850f6204d1ce2162570f671ee37a8f647309ff4a3c919e75"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
