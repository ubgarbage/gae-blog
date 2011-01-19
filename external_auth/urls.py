import django.conf.urls.defaults
import google_login.urls
import mailru_login.urls

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( 'google/', django.conf.urls.defaults.include(google_login.urls) ),
                        ( 'mailru/', django.conf.urls.defaults.include(mailru_login.urls) ),
                        )
