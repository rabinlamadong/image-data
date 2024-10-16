from pydantic_settings import BaseSettings

postgres_uri_string = "postgresql://{user}:{password}@{host}:{port}/{database}"


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "image_data"
    DB_POOL_SIZE: int = 20

    DATABASE_ROLE: str = "postgres"
    IMAGE_DATABASE_SCHEMA: str = "public"

    @property
    def DATABASE_URI(self):
        uri = postgres_uri_string.format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

        return uri

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
