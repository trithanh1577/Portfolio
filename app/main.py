# app/main.py — Session 14 starting point (FastAPI) = the end state of Lab 4.
#
# The port comes from the environment (see the Dockerfile), /health is the fast
# platform health check, and /health/db proves the database connection.
# Session 14, Task C points DATABASE_URL at Supabase WITHOUT changing this file.
# Session 14, Task D then replaces the one-connection-per-request code below
# with a small, self-healing connection pool.
import os

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

APP_VERSION = "1.2.0"  # change this, merge, and watch the pipeline take it live
APP_ENV = os.environ.get("APP_ENV", "development")
DATABASE_URL = os.environ["DATABASE_URL"]  # crash at start if it is missing

app = FastAPI(title="notes")


@app.get("/")
def home():
    return {"app": "notes", "status": "running", "version": APP_VERSION, "env": APP_ENV}


@app.get("/health")
def health():
    # Fast, no login, touches nothing. Render's health check path points here.
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    # Proves the database works. Not the platform health check —
    # on Render it reports an error until Session 14 connects Supabase.
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            n = conn.execute("SELECT count(*) FROM notes").fetchone()[0]
        return {"db": "ok", "notes": n}
    except Exception as err:
        print("health/db failed:", err)  # the detail goes to the logs, not to the browser
        return JSONResponse(status_code=503, content={"db": "error"})
