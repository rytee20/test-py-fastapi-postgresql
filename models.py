from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime

# Таблица с данными о пользователях
class Users(Base):
    __tablename__='users'

    id_user=Column(Integer, primary_key=True, index=True)                       # Идентификатор
    username=Column(String, index=True)                                         # Имя пользователя
    language=Column(String, index=True)                                         # Язык

# Таблица достижений
class Achievements(Base):
    __tablename__='achievements'

    id_achievement=Column(Integer, primary_key=True, index=True)                # Идентификатор
    achievement_name=Column(String, index=True)                                 # Наименование достижения
    scores=Column(Integer, index=True)                                          # Количество очков
    description=Column(String, index=True)                                      # Описание достижения

# Таблица выдачи достижений пользователям
class Users_Achievements(Base):
    __tablename__='users_and_their_achievements'

    id=Column(Integer, primary_key=True, index=True)                            # Идентификатор
    id_user=Column(Integer, ForeignKey("users.id_user"))                        # Идентификатор пользователя
    id_achievement=Column(Integer, ForeignKey("achievements.id_achievement"))   # Идентификатор достижения
    date=Column(DateTime, default=datetime.now())                               # Дата выдачи (по умолчания дата внесения данных в таблицу)