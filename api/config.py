class Config: 
    APP_NAME: str = "Pyfy"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgres://gapi:freeroam@localhost/gofy"
    REDIS_HOST: str = "localhost" 
    REDIS_PORT: int = 6379
    JWT_SECRET: str = "secret_value"
    JWT_ALG: str = "HS256"

config = Config() 