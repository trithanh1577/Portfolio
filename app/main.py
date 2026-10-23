# app/main.py — after Session 14, Task D: one small, self-healing pool.
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool

APP_VERSION = "1.3.0"  # Task D: the visible change for this pull request
APP_ENV = os.environ.get("APP_ENV", "development")
DATABASE_URL = os.environ["DATABASE_URL"]  # crash at start if it is missing

# One pool per running copy of the app. Created closed: tests can import this
# file without a database; the server opens it at start-up (lifespan below).
pool = ConnectionPool(
    DATABASE_URL,
    min_size=1,
    max_size=5,  # small pool: several copies run
    max_lifetime=300,  # recycle: replace after 5 minutes
    check=ConnectionPool.check_connection,  # pre-ping: test before lending
    kwargs={
        "prepare_threshold": None,  # port 6543: no prepared statements
        "connect_timeout": 5,  # fail fast instead of hanging
    },
    open=False,
)


@asynccontextmanager
async def lifespan(app):
    pool.open()  # does not wait: the app starts even if the database is paused
    yield
    pool.close()  # Render stops the container: return the connections cleanly


app = FastAPI(title="notes", lifespan=lifespan)


@app.get("/")
def home():
    return {"app": "notes", "status": "running", "version": APP_VERSION, "env": APP_ENV}


@app.get("/health")
def health():
    # Fast, no login, touches nothing. Render's health check path points here.
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    # Proves the database works. Borrows a connection from the pool for one query.
    try:
        with pool.connection(timeout=5) as conn:
            n = conn.execute("SELECT count(*) FROM notes").fetchone()[0]
        return {"db": "ok", "notes": n}
    except Exception as err:
        print("health/db failed:", type(err).__name__, err)  # details to the logs only
        return JSONResponse(status_code=503, content={"db": "error"})
