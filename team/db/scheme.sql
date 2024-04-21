DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS captain;

CREATE TABLE player
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname  VARCHAR(25)      NOT NULL,
    lastname   VARCHAR(25)      NOT NULL,
    age        TINYINT UNSIGNED NOT NULL,
    experience INT UNSIGNED     NOT NULL
);

CREATE TABLE captain
(
    id    INTEGER PRIMARY KEY,
    grade INT UNSIGNED
)