from databases import Database, DatabaseURL
from .config import config 

async def open_db_conn(): 
    db_url = DatabaseURL(config.DATABASE_URL)
    db = Database(db_url)
    try:
        await db.connect() 
    except Exception as e: 
        raise e 
    return db 

async def close_db_conn(db: Database):
    try: 
        await db.disconnect() 
    except Exception as e: 
        print(e)
     