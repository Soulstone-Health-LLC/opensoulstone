"""
Dictionary for general use
"""

# State Dictionary
STATE_CHOICES = [
    ("", ""),
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("DC", "District of Columbia"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
    ("AS", "American Samoa"),
    ("CZ", "Canal Zone"),
    ("DD", "Department of Defense"),
    ("GU", "Guam"),
    ("FM", "Federated States of Micronesia"),
    ("MH", "Marshall Islands"),
    ("MP", "Northern Mariana Islands"),
    ("PW", "Palau"),
    ("PR", "Puerto Rico"),
    ("UM", "US Minor Outlying Islands"),
    ("NA", "Native American Tribal Authority"),
    ("VI", "Virgin Islands"),
    ("OO", "Other"),
]

# Gender Pronoun Dictionary
GENDER_PRONOUN_CHOICES = [
    ("", ""),
    ("He/Him", "He/Him"),
    ("She/Her", "She/Her"),
    ("They/Them", "They/Them"),
    ("He/Them", "He/Them"),
    ("She/Them", "She/Them"),
    ("Name/Name", "Name/Name"),
    ("Other", "Other"),
]

# Phone Type Dictionary
PHONE_TYPE_CHOICES = [
    ("Mobile", "Mobile"),
    ("Home", "Home"),
    ("Office", "Office"),
    ("Fax", "Fax"),
]

# Role Dictionary
ROLE_CHOICES = [("Practitioner", "Practitioner"), ("Staff", "Staff")]

# User Type Dictionary
USER_TYPE_CHOICES = [
    ("User", "User"),
    ("Super User", "Super User"),
    ("Owner", "Owner"),
]

# Status Dictionary
STATUS_CHOICES = [("Active", "Active"), ("Inactive", "Inactive")]

# Payment Type Dictionary
PAYMENT_TYPE_CHOICES = [
    ("Cash", "Cash"),
    ("Check", "Check"),
    ("Credit Card", "Credit Card"),
    ("Gift Card", "Gift Card"),
    ("Other", "Other"),
]

# Event Type Minutes
EVENT_DURATION_CHOICES = [
    (5, "5 Minutes"),
    (10, "10 Minutes"),
    (15, "15 Minutes"),
    (30, "30 Minutes"),
    (45, "45 Minutes"),
    (60, "1 Hour (60 Minutes)"),
    (75, "1 Hour 15 Minutes (75 Minutes)"),
    (90, "1 Hour 30 Minutes (90 Minutes)"),
    (105, "1 Hour 45 Minutes (105 Minutes)"),
    (120, "2 Hours (120 Minutes)"),
]

# Chakra Score Dictionary
CHAKRA_SCORE_CHOICES = [
    (0, "0"),
    (-5, "-5"),
    (-4, "-4"),
    (-3, "-3"),
    (-2, "-2"),
    (-1, "-1"),
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]
