from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

class UsersBase(BaseModel):
    id_user: int
    username: str
    language: str

class AchievementsBase(BaseModel):
    id_achievement: int
    achievement_name: str
    scores: int
    description: str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Hello, World"}, status_code=200)

@app.post("/achievements/")
async def create_achievements(user:UsersBase, achievement:AchievementsBase, db:db_dependency):
    db_achievement=models.Achievements(achievement_name=achievement.achievement_name, scores=achievement.scores, description=achievement.description)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    db_user=models.Users(username=user.username, language=user.language)
    db.add(db_user)
    db.commit()

