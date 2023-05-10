'''
Dictionary for general use
'''

# State Dictionary
STATE_CHOICES = [('', ''), ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'),
                 ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'),
                 ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'),
                 ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'),
                 ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'),
                 ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'),
                 ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'),
                 ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'),
                 ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'),
                 ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'),
                 ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'),
                 ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'),
                 ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')]

# Gender Pronoun Dictionary
GENDER_PRONOUN_CHOICES = [('', ''),
                          ('He/Him', 'He/Him'),
                          ('She/Her', 'She/Her'),
                          ('They/Them', 'They/Them'),
                          ('He/Them', 'He/Them'),
                          ('She/Them', 'She/Them'),
                          ('Name/Name', 'Name/Name'),
                          ('Other', 'Other')]

# Phone Type Dictionary
PHONE_TYPE_CHOICES = [('Mobile', 'Mobile'),
                      ('Home', 'Home'),
                      ('Office', 'Office'),
                      ('Fax', 'Fax')]

# Role Dictionary
ROLE_CHOICES = [('Practitioner', 'Practitioner'),
                ('Staff', 'Staff')]

# Status Dictionary
STATUS_CHOICES = [('Active', 'Active'),
                  ('Inactive', 'Inactive')]

# Payment Type Dictionary
PAYMENT_TYPE_CHOICES = [('Cash', 'Cash'),
                        ('Check', 'Check'),
                        ('Credit Card', 'Credit Card'),
                        ('Gift Card', 'Gift Card'),
                        ('Other', 'Other')]

# Event Type Minutes
EVENT_DURATION_CHOICES = [(5, '5 Minutes'),
                          (10, '10 Minutes'),
                          (15, '15 Minutes'),
                          (30, '30 Minutes'),
                          (45, '45 Minutes'),
                          (60, '1 Hour (60 Minutes)'),
                          (75, '1 Hour 15 Minutes (75 Minutes)'),
                          (90, '1 Hour 30 Minutes (90 Minutes)'),
                          (105, '1 Hour 45 Minutes (105 Minutes)'),
                          (120, '2 Hours (120 Minutes)')]
