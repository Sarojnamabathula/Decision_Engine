from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Interview Decision Engine"
    api_version: str = "v1"
    environment: str = "development"
    debug: bool = True

    # Rule Engine Settings
    rules_file_path: str = "rules/rules.yaml"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
