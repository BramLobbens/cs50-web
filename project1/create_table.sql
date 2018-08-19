CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       user_name VARCHAR NOT NULL,
       password VARCHAR NOT NULL
       );

CREATE TABLE books (
       id SERIAL PRIMARY KEY,
       isbn VARCHAR NOT NULL,
       title VARCHAR NOT NULL,
       author VARCHAR NOT NULL,
       year VARCHAR NOT NULL
);
