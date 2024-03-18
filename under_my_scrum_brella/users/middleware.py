###########################################################################
#   Author: Luke Clarke
#   Contributors: 
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import UserDetail
from .views import decayHappiness

#Middleware used so happiness decays when any page is accessed
class DecayHappinessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Call the decayHappiness view
        decayHappiness(request)

        return response

