from pydantic import BaseSettings


class Settings(BaseSettings):
    databese_hostname = str
    database_port = str
    database_password = str
    database_name = str
    database_username = str
    secret_key = str
    algorithm = str
    access_token_expire_minutes = int


settings = Settings()
