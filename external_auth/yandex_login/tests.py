from django.test import TestCase, Client
from views import *

class YaUrlsTest(TestCase):

    def setUp(self):
        self.client = Client( HTTP_HOST='test_host' )

    def test_redirect_on_login(self):
        response = self.client.get( '/accounts/external/yandex/login/test_user' )
        self.assertEquals( 302, response.status_code )

    def test_redirects_on_id_in_post(self):
        response = self.client.post( '/accounts/external/yandex/login/', { 'username':'test_user' } )
        self.assertEquals( 302, response.status_code )
        self.assertEquals( 'http://test_host/accounts/external/yandex/login/test_user', response['Location'] ) 
        
