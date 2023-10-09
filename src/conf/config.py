from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql+psycopg2://user:password@localhost:5432/postgres"
    secret_key_jwt: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = "example@meta.ua"
    mail_password: str = "secretPassword"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = "name"
    cloudinary_api_key: int = 12345678
    cloudinary_api_secret: str = "api_secret"


    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Settings()
