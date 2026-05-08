from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Recommendation System"
    environment: str = "development"
    
    # Load settings from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single instance to be imported anywhere in the app
settings = Settings()
