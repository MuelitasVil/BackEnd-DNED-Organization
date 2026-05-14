from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
      env_file='../.env',
      env_file_encoding='utf-8'
    )

    WORKSPACE_MANAGER_URL: str
    MYSQL_USER: str
    MYSQL_ROOT: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_USER_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str


settings = Settings()
