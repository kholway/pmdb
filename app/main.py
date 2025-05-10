from fastapi import FastAPI
from app.routers import movie

app = FastAPI()
app.include_router(movie.router)