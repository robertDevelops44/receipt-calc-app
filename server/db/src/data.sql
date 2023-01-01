DROP table if EXISTS users CASCADE;
DROP table if EXISTS items CASCADE;
DROP table if EXISTS owners CASCADE;

CREATE TABLE users (
    id              SERIAL PRIMARY KEY NOT NULL,
    name            TEXT
);

CREATE TABLE items (
    id              SERIAL PRIMARY KEY NOT NULL,
    store           TEXT,
    name            TEXT,
    tax             FLOAT,
    total_cost      FLOAT,
    cost_per_user   FLOAT
);

CREATE TABLE owners (
    id              SERIAL PRIMARY KEY NOT NULL,
    user_id         INTEGER,
    item_id         INTEGER
);

