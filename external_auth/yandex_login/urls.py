import django.conf.urls.defaults
from views import yandex_login, check_and_auth

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( 'login/(.*)$', yandex_login ),
                        ( 'continue/$', check_and_auth )
                        )

