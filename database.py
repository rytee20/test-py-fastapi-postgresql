from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Подключение к базе данных
URL_DATABASE = 'postgresql://postgres:password@localhost:5432/users_achievements'

# Движок SQLAlchemy для управления подключением к базе данных
engine = create_engine(URL_DATABASE)

# Сессия SQLAlchemy для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для определения моделей SQLAlchemy
Base = declarative_base()
