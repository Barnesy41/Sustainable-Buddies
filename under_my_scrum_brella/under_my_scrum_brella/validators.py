###########################################################################
#   Author: Ollie Barnes
#   Contributors:
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################
from django.core.exceptions import ValidationError
import re

def validate_password(password):
    ''' 
        This function checks that a given password is valid. 
        :param password: the password to validate
    '''
    
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters long.")
    if not re.search('[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search('[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search('[0-9]', password):
        raise ValidationError("Password must contain at least one number letter.")
    if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one symbol (!@#$%^&*(),.?\":{}|<>).")
    