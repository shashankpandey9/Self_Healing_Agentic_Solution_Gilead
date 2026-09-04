from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    ####################################################################
    # Application
    ####################################################################

    app_name: str
    environment: str
    log_level: str

    ####################################################################
    # AWS
    ####################################################################

    aws_region: str
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    ####################################################################
    # DynamoDB
    ####################################################################

    dynamodb_incident_table: str
    dynamodb_audit_table: str
    dynamodb_conversation_table: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()