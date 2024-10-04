from dotenv import load_dotenv
from fastapi import FastAPI
from kitten import router as kitten_router
from breed import router as breen_router

load_dotenv()
app = FastAPI()

app.include_router(breen_router.router, prefix="/breed", tags=["Порода"])
app.include_router(kitten_router.router, prefix="/kitten", tags=["Котёнок"])
