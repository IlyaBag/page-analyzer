DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
name varchar(255) UNIQUE,
created_at date
);
