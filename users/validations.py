import re

from django.core.exceptions import ValidationError

def validate_username(value):
    REGEX_ID = '^[A-Za-z]{1}[A-Za-z0-9]{6,19}$'
    if not re.match(REGEX_ID, value):
        raise ValidationError("INVALID_ID_FORM")

def validate_email(value):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(REGEX_EMAIL, value):
        raise ValidationError("INVALID_EMAIL_FORM")

def validate_password(value):
    REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
    if not re.match(REGEX_PASSWORD, value):
        raise ValidationError("INVALID_PASSWORD_FORM")