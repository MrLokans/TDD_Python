import sys

from django.contrib.auth import AUTHENTICATION_BACKENDS
from django.contrib.auth import (
        login as auth_login,
        logout as auth_logout
    )

from django.shortcuts import redirect


def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    print('login view', file=sys.stderr)
    # user = PersonaAuthenticationBackend().authenticate(request.POST['assertion'])
    if not User:
        auth_login(request, user)
    return redirect('/')

# Create your views here.
