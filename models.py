from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from database import Base

class Users(Base):
    __tablename__='users'

    id_user=Column(Integer, primary_key=True, index=True)
    username=Column(String, index=True)
    language=Column(String, index=True)

class Achievements(Base):
    __tablename__='achievements'

    id_achievement=Column(Integer, primary_key=True, index=True)
    achievement_name=Column(String, index=True)
    scores=Column(Integer, index=True)
    description=Column(String, index=True)

class Users_Achievements(Base):
    __tablename__='users_and_their_achievements'

    id=Column(Integer, primary_key=True, index=True)
    id_user=Column(Integer, ForeignKey("users.id_user"))
    id_achievement=Column(Integer, ForeignKey("achievements.id_achievement"))
    date=Column(DateTime, index=True)