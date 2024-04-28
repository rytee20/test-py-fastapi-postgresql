from sqlalchemy import Boolean, Column, Integer, String
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