from django.conf.urls.defaults import *
from views import google_login, check_and_auth

urlpatterns = patterns( '', 
                        ( 'login/$', google_login ),
                        ( 'continue/$', check_and_auth )
                        )

