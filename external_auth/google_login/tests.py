from django.test import TestCase, Client
from django.contrib.auth.models import User

from views import *
from mock import Mock, patch

class AuthChecker(TestCase):

    def setUp(self):
        urllib2.urlopen = self.fake_urlopen
        self.response_data = [ '' ]

    def set_response_data(self, data):
        self.response_data = data
        
    def fake_urlopen(self, url):
        self.url_used = url
        mock = Mock()
        mock.readlines = Mock( return_value=self.response_data )
        return mock

    def check(self, params, uri):
        checker = GoogleAuthChecker( params, uri )
        return checker.check()

    def test_adds_mode(self):
        self.check( {}, 'test_uri' )
        self.assertEquals( 'test_uri?openid.mode=check_authentication', self.url_used )
        
    def test_adds_response_params(self):
        self.check( { 'param1':'value1', 'param2':'value2' }, 'test_uri' )
        self.assertIn( 'param1=value1', self.url_used )
        self.assertIn( 'param2=value2', self.url_used )
        
    def test_quotes_special_in_params(self):
        self.check( { 'p a':'' }, 'test_uri' )
        self.assertIn( 'p%20a', self.url_used )

    def test_returns_true_on_valid_response(self):
        self.set_response_data( ['is_valid:true'] )
        self.assertTrue( self.check( {}, '' ) )

    def test_returns_false_on_notvalid_response(self):
        self.set_response_data( ['is_valid:false'] )
        self.assertFalse( self.check( {}, '' ) )
        

class GetUserNameTest(TestCase):

    def get( self, email ):
        params = {'openid.ext1.value.email':email}
        return get_username( params )

    def test_gets_username_and_email(self):
        (name, email) = self.get( 'test@mail.com' )
        self.assertEquals( name, 'test' )
        self.assertEquals( email, 'test@mail.com' )

    def test_raises_on_invalid_email(self):
        self.assertRaises( ValueError, self.get, 'testmail.com' )

        
class UrlsTest(TestCase):

    def test_redirect_on_login(self):
        self.client = Client( HTTP_HOST='test_host' )
        response = self.client.get( '/accounts/external/google/login/' )
        self.assertEquals( 302, response.status_code )

