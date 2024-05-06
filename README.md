# test-py-fastapi-postgresql

Тестовое задание [здесь](https://github.com/rytee20/test-py-fastapi-postgresql/blob/main/тестовое_сов_07_03_24.pdf)

Таблицы:
-----------

- **Пользователи**
  - id_user (Идентификатор)
  - username (Имя пользователя)
  - language (Язык)
  
- **Достижения**
  - id_achievement (Идентификатор)
  - achievement_name (Наименование достижения)
  - scores (Количество очков)
  - description (Описание достижения)
  
- **Пользователи и их достижения**
  - id (Идентификато)
  - id_user (Идентификатор пользователя)
  - id_achievement (Идентификатор достижения)
  - date (Дата выдачи)
 
Таблица для отслеживания того, какие пользователь имеет достижения.
 
Функционал:
-----------

- Добавление нового достижения

```
@app.post("/users_achievements/achievements/create")
async def create_achievement(achievement_name:str, scores:int, description:str, db:Session = Depends(get_db))
```

- Добавление нового пользователя

```
@app.post("/users_achievements/users/create")
async def create_user(username: str, language: Language, db: Session = Depends(get_db))
```
Для языка предоставляются варианты:

![image](https://github.com/rytee20/test-py-fastapi-postgresql/assets/94058290/760d0578-dbd3-4767-ae02-f0017dba3eb2)

- Присвоение достижения пользователю

```
@app.post("/users_achievements/set_achievement")
async def set_achievement(id_user:int, id_achievement:int, db: Session = Depends(get_db))
```

Добавить одному и тому же пользователь два одинаковых достижения нельзя. Дата по умолчанию будет равна дате внесения записи в таблицу.

- Предоставление данных о пользователе

```
@app.get("/users_achievements/users/{id_user}")
async def get_user(id_user: int, db: Session = Depends(get_db))
```

- Предоставление данных о всех возможных достижениях

```
@app.get("/users_achievements/achievements")
async def get_all_achievements(db: Session = Depends(get_db))
```
Выводятся данные о заданном пользователе: id, никнейм, язык.

- Предоставления данных о достижения конкретного пользователя на его языке

```
@app.get("/users_achievements/users/{id_user}/achievements")
async def get_users_achievements(id_user: int, db: Session = Depends(get_db))
```
Выводятся все достижения (id, название, очки, описание), полученные пользователем с переводом на язык пользователя.

- Предоставление данных о пользователях с максимальным количеством достижений

```
@app.get("/users_achievements/users_with_max_achievements")
async def get_users_with_max_achievements(db: Session = Depends(get_db))
```
Выводятся двнные (id, никнейм, количество достижений) о пользователе (или пользователях, если таковых несколько) с наибольшим количеством достижений. 

- Предоставление данных о пользователях с максимальным количеством очков

```
@app.get("/users_achievements/users_with_max_scores")
async def get_users_with_max_scores(db: Session = Depends(get_db))
```
Выводятся данные (id, никнейм, количество очков) о пользователе (или пользователях, если таковых несколько) с наибольшим количеством очков. 

- Предоставление данных о пользователях с максимальной разницей очков достижений

```
@app.get("/users_achievements/users_with_max_difference")
async def get_users_with_max_difference(db: Session = Depends(get_db))
```
Выводятся данные (id, никнейм, количество очков, разница) о пользователе (или пользователях, если таковых несколько) с наибольшей разницей между максимальным возможным для получения количеством очков и количеством очков, полученным пользователями. 

- Предоставление данных о пользователях с минимальной разницей очков достижений

```
@app.get("/users_achievements/users_with_min_difference")
async def get_users_with_min_difference(db: Session = Depends(get_db))
```
Выводятся данные (id, никнейм, количество очков, разница) о пользователе (или пользователях, если таковых несколько) с наименьшей разницей между максимальным возможным для получения количеством очков и количеством очков, полученным пользователями.

- Предоставление данных о пользователях, которые за последние 7 дней каждый день получали хотя бы одно достижение

```
@app.get("/users_achievements/users_with_7days_achievements")
async def get_users_with_7days_achievements(db: Session = Depends(get_db))
```
Выводятся данные (id, никнейм) о пользователях, которые за последние 7 дней получали хотя бы одно достижение каждый день.
