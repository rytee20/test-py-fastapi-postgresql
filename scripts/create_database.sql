DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS achievements CASCADE;
DROP TABLE IF EXISTS users_and_their_achievements CASCADE;

CREATE TABLE users(
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    language VARCHAR(20) NOT NULL CHECK (language IN ('ru', 'en'))
);

CREATE TABLE achievements(
    id_achievement SERIAL PRIMARY KEY,
    achievement_name VARCHAR(20) NOT NULL,
    scores INTEGER NOT NULL,
	description VARCHAR(100) NOT NULL
);

CREATE TABLE users_and_their_achievements(
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    id_achievement INTEGER NOT NULL,
	date DATE NOT NULL DEFAULT (CURRENT_DATE),
	UNIQUE (id_user, id_achievement)
);