from fastapi import FastAPI
import redis 

from .db import open_db_conn, close_db_conn
from .limiter import limiter
from .config import config 

def start_application(app: FastAPI) -> callable: 
    async def start() -> None: 
        db = await open_db_conn() 
        rds = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=False)
        
        app.state.limiter = limiter 
        app.state._db = db
        app.state._redis = rds 
    return start 

def stop_application(app: FastAPI) -> callable: 
    async def stop() -> None: 
        db = app.state._db 
        await close_db_conn(db)
    return stop 