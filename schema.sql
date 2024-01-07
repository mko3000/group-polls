CREATE TABLE polls_users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE polls_groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator INTEGER REFERENCES polls_users
);

CREATE TABLE polls_group_members (
    group_id INTEGER REFERENCES polls_groups,
    user_id INTEGER REFERENCES polls_users
);

CREATE TABLE polls_polls (
    id SERIAL PRIMARY KEY,
    name TEXT,
    group_id INTEGER REFERENCES polls_groups,
    created_at TIMESTAMP,
    closes_at TIMESTAMP
);

CREATE TABLE polls_choices (
    id SERIAL PRIMARY KEY,
    name TEXT,
    added_by INTEGER REFERENCES polls_users,
    votes INTEGER --this maybe not needed
);

CREATE TABLE polls_user_votes (
    choice_id INTEGER REFERENCES polls_choices,
    user_id INTEGER REFERENCES polls_users
);