from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expires_minutes: str

    class Config:
        env_file = ".env"


settings = Settings()
