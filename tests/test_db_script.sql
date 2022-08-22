/* insert test data for practice table */
INSERT INTO
  practice (
    name,
    email,
    website,
    phone_number,
    phone_type,
    address_1,
    address_2,
    city,
    state,
    zipcode,
    status
  )
VALUES
  (
    'Healing Hands',
    'healinghands@email.com',
    'healinghands.com',
    5555555555,
    'Office',
    '123 Main Street',
    'Suite 200',
    'San Diego',
    'CA',
    92121,
    'Active'
  );

/* insert test support user */
INSERT INTO
  user (
    practice_id,
    email,
    password,
    first_name,
    last_name,
    role,
    status
  )
VALUES
  (
    1,
    'rodneygauna+support@gmail.com',
    'rodneygauna+support',
    'Support',
    'Test User',
    'Support',
    'Active'
  );