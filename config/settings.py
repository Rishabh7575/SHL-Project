from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings class to load environment variables.
    Using pydantic-settings ensures our environment variables are validated.
    """
    app_name: str = "AI Recommendation System"
    environment: str = "development"
    
    # Allows loading from a .env file, without crashing if it's missing
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# A global instance of our settings to be imported where needed
settings = Settings()
