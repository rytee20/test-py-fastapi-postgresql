from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import datetime

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
async def create_achievement(achievement:AchievementsBase, db:db_dependency):
    db_achievement=models.Achievements(achievement_name=achievement.achievement_name, scores=achievement.scores, description=achievement.description)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)

@app.post("/users_achievements/users/create")
async def create_user(user:UsersBase, db:db_dependency):
    db_user=models.Users(username=user.username, language=user.language)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

@app.post("/users_achievements/set_achievement")
async def set_achievements(u_a:UsersAchievementsBase, db:db_dependency):
    db_u_a=models.Users(id_user=u_a.id_user, id_achievement=u_a.id_achievement, date=datetime.now())
    db.add(db_u_a)
    db.commit()
    db.refresh(db_u_a)

