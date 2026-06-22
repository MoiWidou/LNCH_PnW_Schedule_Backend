from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from db import engine
from models import Member, SQLModel
from routes import router

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(router)