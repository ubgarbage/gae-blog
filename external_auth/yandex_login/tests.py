from django.test import TestCase, Client
from views import *

class MailruUrlsTest(TestCase):

    def setUp(self):
        self.client = Client( HTTP_HOST='test_host' )

    def test_redirect_on_login(self):
        response = self.client.get( '/accounts/external/mailru/login/test_user' )
        self.assertEquals( 302, response.status_code )

    def test_redirects_on_id_in_post(self):
        response = self.client.post( '/accounts/external/mailru/login/', { 'username':'test_user' } )
        self.assertEquals( 302, response.status_code )
        self.assertEquals( 'http://test_host/accounts/external/mailru/login/test_user', response['Location'] ) 
        


class MailruIdTest(TestCase):
    
    def test_returns_user_id(self):
        self.assertEquals( 'test_user', get_user_id( 'http://openid.mail.ru/mail/test_user' ) )

    def test_throws_on_empty(self):
        with self.assertRaises( Exception ):
            get_user_id( 'http://openid.mail.ru/mail/' )

    def test_throws_on_invalid(self):
        with self.assertRaises( Exception ):
            get_user_id( 'http://openid.asdfasdfasd/' )

