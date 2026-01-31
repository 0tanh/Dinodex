CREATE TABLE requests (
    TEXT
);

CREATE TABLE myDinos (
    images BLOB,
    imageURL TEXT,
    description TEXT UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL,
    collected_date TEXT)

CREATE