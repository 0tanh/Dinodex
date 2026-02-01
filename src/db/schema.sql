CREATE TABLE requests (
    request TEXT,
    response BLOB,
    response_status INT,
    url TEXT,
    elapsed TEXT,
    re
);

CREATE TABLE myDinos (
    image BLOB,
    imageURL TEXT,
    description TEXT UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL,
    collected_date TEXT,
    copies INT,
    rare BOOL
);

INSERT INTO requests VALUES ()