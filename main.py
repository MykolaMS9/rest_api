import time

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.conf.config import settings
from src.database.db import get_db
from src.routes import contacts, auth, users
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['perfomance'] = str(during)
    return response


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=1, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
async def root(request: Request):
    return {'message': 'Hello world!'}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

# alembic revision --autogenerate -m 'Init'

# alembic upgrade head

# uvicorn main:app --reload


# for start

# alembic revision --autogenerate -m "Add confirmed users"
# uvicorn main:app --host localhost --port 8500 --reload

# docker-compose up
