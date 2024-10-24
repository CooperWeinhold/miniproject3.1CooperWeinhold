DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS aircrafts;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE aircrafts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  aircraft_type TEXT NOT NULL,
  manufacturer TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
