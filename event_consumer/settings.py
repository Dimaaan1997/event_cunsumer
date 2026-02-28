import os
import time

from pydantic import ConfigDict, Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_url: str = Field(validation_alias="KAFKA_URL")
    START_TIME: float = time.time()
    app_debug: bool = Field(validation_alias="APP_DEBUG")

    like_topic: str = Field(validation_alias='LIKE_TOPIC')
    playlist_topic: str = Field(validation_alias='PLAYLIST_TOPIC')
    listen_topic: str = Field(validation_alias='LISTEN_TOPIC')

    model_config = ConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
    )


settings = Settings()
