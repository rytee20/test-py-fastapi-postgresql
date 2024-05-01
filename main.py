from enum import Enum
from fastapi import Body, FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import Path

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

class UsersAchievementsBase(BaseModel):
    id: int
    id_user: List[UsersBase]
    id_achievement: List[AchievementsBase]
    date: datetime
    class Config:
        arbitrary_types_allowed = True

class Language(str, Enum):
    ru = "ru"
    en = "en"

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/users_achievements/users/{id_user}")
async def get_user(id_user: int, db: db_dependency):
    result =db.query(models.Users).filter(models.Users.id_user==id_user).first()
    if not result:
        raise HTTPException (status_code=404,detail='User is not found')
    return result

@app.get("/users_achievements/achievements", response_model=List[AchievementsBase])
async def get_all_achievements(db: db_dependency):
    result = db.query(models.Achievements).all()
    if not result:
        raise HTTPException (status_code=404,detail='Achievements is not found')
    return result

@app.post("/users_achievements/achievements/create")
async def create_achievement(achievement_name:str, scores:int, description:str, db:db_dependency):
    db_achievement=models.Achievements(achievement_name=achievement_name, scores=scores, description=description)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)

@app.post("/users_achievements/users/create")
async def create_user(db: db_dependency, username: str, language: Language = Path(..., title="The language of the user", description="Choose the language of the user", example="ru")):
    db_user = models.Users(username=username, language=language.value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

@app.post("/users_achievements/set_achievement")
async def set_achievement(id_user:int, id_achievement:int, db:db_dependency):
    db_u_a=models.Users_Achievements(id_user=id_user, id_achievement=id_achievement)
    db.add(db_u_a)
    db.commit()
    db.refresh(db_u_a)

