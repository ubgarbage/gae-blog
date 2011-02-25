import django.conf.urls.defaults
import google_login.urls
import mailru_login.urls
import yandex_login.urls
import inboxru_login.urls

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( 'google/', django.conf.urls.defaults.include(google_login.urls) ),
                        ( 'mailru/', django.conf.urls.defaults.include(mailru_login.urls) ),
                        ( 'inboxru/', django.conf.urls.defaults.include(inboxru_login.urls) ),
                        ( 'yandex/', django.conf.urls.defaults.include(yandex_login.urls) ),
                        )
