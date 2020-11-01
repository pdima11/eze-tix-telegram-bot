DROP TABLE IF EXISTS ezetixbot.requests;
DROP TABLE IF EXISTS ezetixbot.users;
DROP TYPE IF EXISTS REQUEST_STATUS;
DROP SCHEMA IF EXISTS ezetixbot;


CREATE SCHEMA ezetixbot;

CREATE TYPE REQUEST_STATUS AS ENUM ('CREATED', 'IN PROGRESS', 'CLOSED');

CREATE TABLE ezetixbot.users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(50),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	is_bot BOOLEAN NOT NULL,
	language_code VARCHAR(2) NOT NULL,
	last_visit TIMESTAMP without time zone DEFAULT NOW()
);

CREATE TABLE ezetixbot.requests (
	request_id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL,
	transporter VARCHAR(20) NOT NULL,
	departure VARCHAR(20) NOT NULL,
	arrival VARCHAR(20) NOT NULL,
	required_date DATE NOT NULL,
	from_time VARCHAR(5) NOT NULL,
	to_time VARCHAR(5) NOT NULL,
	status REQUEST_STATUS NOT NULL,
	created_at TIMESTAMP without time zone DEFAULT NOW(),
	closed_at TIMESTAMP without time zone
)