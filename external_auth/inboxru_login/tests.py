from django.test import TestCase, Client
from views import *

class MailruUrlsTest(TestCase):

    def setUp(self):
        self.client = Client( HTTP_HOST='test_host' )

    def test_redirect_on_login(self):
        response = self.client.get( '/accounts/external/inboxru/login/test_user' )
        self.assertEquals( 302, response.status_code )

    def test_redirects_on_id_in_post(self):
        response = self.client.post( '/accounts/external/inboxru/login/', { 'username':'test_user' } )
        self.assertEquals( 302, response.status_code )
        self.assertEquals( 'http://test_host/accounts/external/inboxru/login/test_user', response['Location'] ) 
        
