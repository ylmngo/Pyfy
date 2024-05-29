import time

from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .routes import router 
from .db import open_db_conn
from .tasks import start_application, stop_application
from .config import config 


def get_application(): 
    app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION) 

    app.add_event_handler("startup", start_application(app))    
    app.add_event_handler("shutdown", stop_application(app))    

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.include_router(router=router, prefix="/api")
    return app 

app = get_application() 

@app.middleware("http")
async def process_time(req: Request, next): 
    start = time.time()
    response = await next(req) 
    stop = time.time() 
    response.headers["X-process-time"] = str(stop - start) 
    print(req.url, stop - start)
    return response 