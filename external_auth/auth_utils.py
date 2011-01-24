import django

def authenticate_without_pass( name, email, request ):
    #passing email and nopass parameters to external_auth.auth_backends.NoPassBackend
    user = django.contrib.auth.authenticate( username=name, email=email, nopass=True )
    if None != user:
        django.contrib.auth.login( request, user )
