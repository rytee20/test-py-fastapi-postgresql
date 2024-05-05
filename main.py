from enum import Enum
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from mtranslate import translate as mtranslate
from sqlalchemy import func
from sqlalchemy import case

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
    result = db.query(models.Users).filter(models.Users.id_user==id_user).first()
    if not result:
        raise HTTPException (status_code=404,detail='User is not found')
    return result

@app.get("/users_achievements/achievements", response_model=List[AchievementsBase])
async def get_all_achievements(db: db_dependency):
    result = db.query(models.Achievements).all()
    if not result:
        raise HTTPException (status_code=404,detail='Achievements is not found')
    return result

@app.get("/users_achievements/users/{id_user}/achievements")
async def get_users_achievements(id_user: int, db: db_dependency):
    result = db.query(models.Achievements).join(models.Users_Achievements).filter(models.Users_Achievements.id_user==id_user).all()

    if not result:
        raise HTTPException (status_code=404,detail='Achievements is not found')

    user = db.query(models.Users).filter(models.Users.id_user == id_user).first()

    translated_achievements = []
    for achievement in result:
        translated_achievement = {
            "id_achievement": achievement.id_achievement,
            "achievement_name": mtranslate(achievement.achievement_name, user.language),
            "scores": achievement.scores,
            "description": mtranslate(achievement.description, user.language)
        }
        translated_achievements.append(translated_achievement)

    return translated_achievements

@app.get("/users_achievements/users_with_max_achievements")
async def get_users_with_max_achievements(db: db_dependency):
    user_achievements_count = db.query(models.Users_Achievements.id_user, func.count().label("achievements_count")).group_by(models.Users_Achievements.id_user).subquery()

    max_achievements_count = db.query(
        func.max(user_achievements_count.c.achievements_count)).scalar()

    users_with_max_achievements = db.query(models.Users).join(user_achievements_count, models.Users.id_user == user_achievements_count.c.id_user).filter(user_achievements_count.c.achievements_count == max_achievements_count).all()

    if not users_with_max_achievements:
        raise HTTPException (status_code=404,detail='Users is not found')

    result = []
    for user in users_with_max_achievements:
        r = {
            "id_user": user.id_user,
            "username": user.username,
            "count_achievements": max_achievements_count
        }
        result.append(r)

    return result

@app.get("/users_achievements/users_with_max_scores")
async def get_users_with_max_scores(db: db_dependency):
    user_scores = (
        db.query(
            models.Users_Achievements.id_user,
            func.sum(models.Achievements.scores).label("total_scores")
        )
        .join(models.Achievements, models.Users_Achievements.id_achievement == models.Achievements.id_achievement)
        .group_by(models.Users_Achievements.id_user)
        .subquery()
    )

    max_scores = db.query(func.max(user_scores.c.total_scores)).scalar()

    users_with_max_scors = db.query(models.Users).join(user_scores, models.Users.id_user == user_scores.c.id_user).filter(user_scores.c.total_scores == max_scores).all()

    if not users_with_max_scors:
        raise HTTPException (status_code=404,detail='Users is not found')
    
    result = []
    for user in users_with_max_scors:
        r = {
            "id_user": user.id_user,
            "username": user.username,
            "total_scores": max_scores
        }
        result.append(r)
    
    return result

@app.get("/users_achievements/users_with_max_difference")
async def get_users_with_max_difference(db: db_dependency):
    max_scores=db.query(func.sum(models.Achievements.scores)).scalar()

    user_scores = (
        db.query(
            models.Users_Achievements.id_user,
            func.sum(models.Achievements.scores).label("total_scores"),
            (max_scores-func.sum(models.Achievements.scores)).label("difference")
        )
        .join(models.Achievements, models.Users_Achievements.id_achievement == models.Achievements.id_achievement)
        .group_by(models.Users_Achievements.id_user)
        .subquery()
    )

    max_difference=db.query(func.max(user_scores.c.difference)).scalar()

    users_with_max_diff=(
        db.query(user_scores.c.id_user, models.Users.username, user_scores.c.total_scores, user_scores.c.difference)
        .filter(models.Users.id_user==user_scores.c.id_user)
        .filter(user_scores.c.difference==max_difference)
        .all())
    
    if not users_with_max_diff:
        raise HTTPException (status_code=404,detail='Users is not found')

    result = [{"id_user": id_user,  "username": username, "total_scores": total_scores, "difference": difference} 
              for id_user, username, total_scores, difference in users_with_max_diff]

    return result

@app.get("/users_achievements/users_with_min_difference")
async def get_users_with_min_difference(db: db_dependency):
    max_scores=db.query(func.sum(models.Achievements.scores)).scalar()

    user_scores = (
        db.query(
            models.Users_Achievements.id_user,
            func.sum(models.Achievements.scores).label("total_scores"),
            (max_scores-func.sum(models.Achievements.scores)).label("difference")
        )
        .join(models.Achievements, models.Users_Achievements.id_achievement == models.Achievements.id_achievement)
        .group_by(models.Users_Achievements.id_user)
        .subquery()
    )

    min_difference=db.query(func.min(user_scores.c.difference)).scalar()

    users_with_max_diff=(
        db.query(user_scores.c.id_user, models.Users.username, user_scores.c.total_scores, user_scores.c.difference)
        .filter(models.Users.id_user==user_scores.c.id_user)
        .filter(user_scores.c.difference==min_difference)
        .all())
    
    if not users_with_max_diff:
        raise HTTPException (status_code=404,detail='Users is not found')

    result = [{"id_user": id_user, "username": username, "total_scores": total_scores, "difference": difference} 
              for id_user, username, total_scores, difference in users_with_max_diff]

    return result

@app.get("/users_achievements/users_with_7days_achievements")
async def get_users_with_7days_achievements(db: db_dependency):

    today_date = datetime.now()

    get_users_count_achievements = (
        db.query(
            models.Users_Achievements.id_user,
            func.date(models.Users_Achievements.date).label("date")
        )
        .filter(models.Users_Achievements.date >= today_date - timedelta(days=6))
        .filter(models.Users_Achievements.date <= today_date)
        .subquery()
    )

    get_users_count_7days_achievements = (
        db.query(
            get_users_count_achievements.c.id_user,
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date - timedelta(days=6)), 1),else_ =0)).label("day1"),
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date - timedelta(days=5)), 1),else_ =0)).label("day2"),
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date - timedelta(days=4)), 1),else_ =0)).label("day3"),
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date - timedelta(days=3)), 1),else_ =0)).label("day4"),
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date - timedelta(days=2)), 1),else_ =0)).label("day5"),
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date - timedelta(days=1)), 1),else_ =0)).label("day6"),
            func.sum(case((func.date(get_users_count_achievements.c.date) == func.date(today_date), 1),else_ =0)).label("day7"),
        )
        .group_by(get_users_count_achievements.c.id_user)
        .subquery()
    )

    get_users_with_7days_achievements = (
        db.query(
            get_users_count_7days_achievements.c.id_user,
            func.sum(case((get_users_count_7days_achievements.c.day1 != 0 and
                        get_users_count_7days_achievements.c.day2 != 0 and
                        get_users_count_7days_achievements.c.day3 != 0 and
                        get_users_count_7days_achievements.c.day4 != 0 and
                        get_users_count_7days_achievements.c.day5 != 0 and
                        get_users_count_7days_achievements.c.day6 != 0 and
                        get_users_count_7days_achievements.c.day7 != 0, 1), else_=0)
            ).label("achievements_in_sequence")
        )
        .group_by(get_users_count_7days_achievements.c.id_user)
        .subquery()
    )

    users = (
        db.query(
            get_users_with_7days_achievements.c.id_user,
            models.Users.username
        )
        .filter(get_users_with_7days_achievements.c.id_user==models.Users.id_user)
        .filter(get_users_with_7days_achievements.c.achievements_in_sequence!=0)
        .all()
    )

    if not users:
        raise HTTPException (status_code=404,detail='Users is not found')

    result = [{"id_user": id_user, "username": username} 
            for id_user, username in users]

    return result


@app.post("/users_achievements/achievements/create")
async def create_achievement(achievement_name:str, scores:int, description:str, db:db_dependency):
    db_achievement = models.Achievements(achievement_name=achievement_name, scores=scores, description=description)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)

@app.post("/users_achievements/users/create")
async def create_user(db: db_dependency, username: str, language: Language):
    db_user = models.Users(username=username, language=language.value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

@app.post("/users_achievements/set_achievement")
async def set_achievement(id_user:int, id_achievement:int, db:db_dependency):
    db_u_a = models.Users_Achievements(id_user=id_user, id_achievement=id_achievement)
    db.add(db_u_a)
    db.commit()
    db.refresh(db_u_a)

