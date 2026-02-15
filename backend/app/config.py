from pydantic_settings import BaseSettings

# Configuration Management using Pydantic Settings
# This class reads environment variables and provides defaults.
# It ensures type safety and standard way to access configuration.

class Settings(BaseSettings):
    app_name: str = "Interview Performance Analyzer API"
    debug: bool = True
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "change_this_secret_key"
    
    # AWS Storage Config
    aws_access_key_id: str = "placeholder_key"
    aws_secret_access_key: str = "placeholder_secret"
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "interview-recordings-bucket"
    use_s3_storage: bool = False  # Feature flag to enable/disable easily

    class Config:
        env_file = ".env"

settings = Settings()
