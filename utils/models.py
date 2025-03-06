from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_id: str = Field(min_length=14, alias="app_id")
    client_secret: str = Field(min_length=27, alias="app_secret")
    user_agent: str = Field(alias="app_name")
    redirect_uri: str = Field(default="http://localhost:8080")
    ratelimit_seconds: int = Field(default=10, alias="ratelimit_seconds")

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


class IncomingArgs(BaseSettings, cli_parse_args=True):
    topic: str = Field(min_length=1)
    limit: int = Field(default=5)
