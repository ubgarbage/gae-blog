import django.conf.urls.defaults
from external_auth.openid_auth import OpenIdAuthenticator

openid_authenticator = OpenIdAuthenticator( 'http://openid.mail.ru/mail/', '', 'mail.ru' )

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( 'login/(.*)$', openid_authenticator.openid_login ),
                        ( 'continue/$', openid_authenticator.check_and_auth )
                        )

