DROP table if EXISTS people CASCADE;
DROP table if EXISTS items CASCADE;

CREATE TABLE people (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT,
    total FLOAT
)

CREATE TABLE items (
    id SERIAL PRIMARY KEY NOT NULL,
    store TEXT,
    name TEXT,
    tax FLOAT,
    total_cost FLOAT,
    cost_per_user FLOAT,
    user_id
)

