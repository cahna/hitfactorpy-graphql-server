from pydantic import BaseSettings, Field, PostgresDsn


class HitFactorConfig(BaseSettings):
    SQLALCHEMY_POSTGRES_DSN: PostgresDsn = Field("postgresql+asyncpg://postgres:postgres@localhost:5432/hitfactorpy")
    ALEMBIC_POSTGRES_DSN: PostgresDsn = Field("postgresql+psycopg2://postgres:postgres@localhost:5432/hitfactorpy")

    class Config:
        env_prefix = "HF_"
