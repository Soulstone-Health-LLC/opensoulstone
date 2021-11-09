/* only drops the person table if it exists */
DROP TABLE IF EXISTS practice;


/* create practice table */
CREATE TABLE practice (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    website TEXT,
    phone_number INTEGER,
    phone_type VARCHAR(10),
    timezone_id INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    updated_by INTEGER
);


/* insert test data for practice table */
INSERT INTO practice (
    name,
    email,
    website,
    phone_number,
    phone_type,
    timezone_id,
    created_at,
    updated_at,
    updated_by)
VALUES (
    'Healing Hands',
    'healinghands@email.com',
    'healinghands.com',
    5555555555,
    'office',
    5,
    '2021-10-31 12:00:00',
    '2021-10-31 12:00:00',
    1
);