import django.conf.urls.defaults
from views import mailru_login, check_and_auth

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( 'login/(.*)$', mailru_login ),
                        ( 'continue/$', check_and_auth )
                        )

