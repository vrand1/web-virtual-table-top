from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #Параметры подключения к базе данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    #Авторизация через Discord
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str
    #JWT, фронтенд
    JWT_SECRET: str
    FRONTEND_URL: str
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    
    
    
    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    @property
    def DATABASE_URL_sync(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
    )

settings = Settings()
print(f"DEBUG: DB_PASS as hex: {settings.DB_PASS.encode('utf-8').hex()}")