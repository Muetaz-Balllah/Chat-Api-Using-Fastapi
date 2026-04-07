from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    SECRET_ALGORITEM: str
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
     
    model_config = SettingsConfigDict (
        env_file= ".env",
        extra= 'ignore'
    )



Config = Settings()