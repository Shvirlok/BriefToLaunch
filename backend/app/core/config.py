from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings for the Cynical CMO Campaign Strategy MVP.
    Loads variables from environment or .env, falling back to dummy keys.
    """
    OPENAI_API_KEY: str = Field("sk-dummy-hackathon-key-placeholder", description="Official OpenAI API Key.")
    OPENAI_MODEL: str = Field("gpt-4o", description="Default OpenAI model to query.")
    APP_PORT: int = Field(8000, description="FastAPI server port.")

    @field_validator("OPENAI_API_KEY", mode="before")
    @classmethod
    def fallback_to_placeholder(cls, v: str) -> str:
        # If the key is empty or whitespace-only (e.g. in .env), fall back to placeholder
        if not v or v.strip() == "":
            return "sk-dummy-hackathon-key-placeholder"
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
