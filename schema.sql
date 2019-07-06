drop table movies

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    genre TEXT NOT NULL,
    tags TEXT NOT NULL,
    poster TEXT NOT NULL,
    likes INTEGER NOT NULL DEFAULT 0
);
