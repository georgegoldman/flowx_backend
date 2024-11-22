from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict
)
from pydantic import Field

class Settngs(BaseSettings):
    APP_NAME: str
    API_VERSION:str
    
    # MongoDB settings
    MONGO_DB_URL: str = Field(..., description="MongoDB connection URL") #type: ignore  # noqa: F821
    DB_NAME: str = Field("aleaf", description="Database name") #type: ignore  # noqa: F821

    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_DAY:int
    MONGO_DB_URL:str #type: ignore

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env",
        env_file_encoding="utf-8"
    )

    @classmethod
    def settings_customise_sources(cls, settings_cls: type[BaseSettings], init_settings: PydanticBaseSettingsSource, env_settings: PydanticBaseSettingsSource, dotenv_settings: PydanticBaseSettingsSource, file_secret_settings: PydanticBaseSettingsSource) -> tuple[PydanticBaseSettingsSource, ...]:
        return super().settings_customise_sources(settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings)
    
# Instantiate the settings
settings = Settngs() #type: ignore