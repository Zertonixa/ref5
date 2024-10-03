from typing import Union
import os
import json
import time
import asyncio
import asyncpg
from dotenv import load_dotenv
import psycopg2
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI, Response, openapi
from kitten import router as kitten_router
from breed import router as breen_router

load_dotenv()
app = FastAPI()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")


# def connect_to_db():
#     retries = 5
#     while retries > 0:
#         try:
#             conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER,password=POSTGRES_PASSWORD,host="db",port=5432)
#             return conn
#         except:
#             retries -= 1
#             # time.sleep(5)
#     raise Exception("Could not connect to the database")

# conn = connect_to_db()

conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="db", port=5432)
cursor = conn.cursor()

# db = configure_asyncpg(app, "postgresql://postgres:postgres@localhost/db")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/kittens", summary="get all kittens test")
def read_root():
    cursor.execute("SELECT * from kittens")
    rows = cursor.fetchall()
    result_json = json.dumps(rows, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    return Response(content=result_json, media_type="application/json")
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(kitten_router.router, prefix="/kitten", tags=["Kitten"])
