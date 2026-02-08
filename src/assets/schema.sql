CREATE TABLE requests (
    request BLOB,
    response BLOB,
    response_status INT,
    url TEXT,
    elapsed TEXT,
    collected_date TEXT
);

CREATE TABLE myDinos (
    name TEXT UNIQUE NOT NULL PRIMARY KEY,
    species TEXT UNIQUE,
    image BLOB,
    imageURL TEXT,
    description TEXT NOT NULL,
    collected_date TEXT
);

CREATE TABLE allDinos (
    species TEXT UNIQUE PRIMARY KEY,
    copies INT,
    rare BOOL,
    collected_date TEXT
)

CREATE TABLE stats (
    catches INT,
    unsucessful INT
)