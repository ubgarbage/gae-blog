from django.test import TestCase
from django.contrib.auth.models import User
from mock import Mock, patch
from auth_backends import NoPassBackend
from utils import *
from google_login.tests import *
from mailru_login.tests import *
from models import AllowedUser
from openid_auth import OpenIdAuthenticator


class NoPassTest(TestCase):

    def setUp(self):
        self.back = NoPassBackend()
        AllowedUser.objects.create( username='test' )
        AllowedUser.objects.create( username='test2' )
    
    def test_return_none_if_password( self ):
        self.assertEquals( None, self.back.authenticate( 'test', 'test' ) )

    def test_create_user_ifdoesnt_exist_on_nopass( self ):
        user_auth = self.back.authenticate( 'test2', '', nopass = True, email='test@mail.ru' )
        user = User.objects.get( username='test2' )
        self.assertEquals( user_auth, user )

    def test_return_existing_user_if_exists_on_nopass( self ):
        User.objects.create_user( 'test2', 'test2@mail.ru' )
        user = self.back.authenticate( 'test2', '', nopass = True )
        self.assertEquals( 'test2', user.username )
        self.assertEquals( 'test2@mail.ru', user.email )

    def test_return_none_on_not_allowed( self ):
        self.assertEquals( None, self.back.authenticate( 'test3', 'test' ) )

    def test_case_insensitive_check( self ):
        user_auth = self.back.authenticate( 'Test', '', nopass = True )
        self.assertEquals( 'test', user_auth.username )

@patch( 'django.contrib.auth.models.User.objects.create_user' )
@patch( 'django.contrib.auth.login' )
class AuthTest(TestCase):

    def auth( self, name, email ):
        AllowedUser.objects.create( username='test' )
        AllowedUser.objects.create( username='' )
        request_mock = Mock()
        authenticate_without_pass( name, email, request_mock )
        return request_mock

    def test_gets_username_from_request(self, login_mock, create_user_mock):
        self.auth( 'test', 'test@mail.com' )
        create_user_mock.assert_called_with( 'test', 'test@mail.com' )

    def test_empty_username(self, login_mock, create_user_mock):
        self.auth( '', '@mail.com' )
        create_user_mock.assert_called_with( '', '@mail.com' )

    @patch( 'django.contrib.auth.models.User.objects.get' )
    def test_doesnt_create_if_exists(self, get_mock, login_mock, create_user_mock):
        get_mock.return_value = Mock()
        self.auth( 'test', 'test@mail.com' )
        self.assertEquals( 0, create_user_mock.call_count )

    def test_login_user(self, login_mock, create_user_mock):
        create_user_mock.return_value = Mock()
        request_mock = self.auth( 'test', 'test@mail.ru' )
        login_mock.assert_called_with( request_mock, create_user_mock.return_value )

    def test_login_not_allowed(self, login_mock, create_user_mock):
        create_user_mock.return_value = Mock()
        request_mock = self.auth( 'test3', 'test@mail.ru' )
        self.assertFalse( login_mock.called )
        


class OpenidGetUserTest(TestCase):
    
    def setUp(self):
        self.openidauth = OpenIdAuthenticator( 'http://openid.lalala.ru/mail/', '/', 'lalala.ru' )

    def test_returns_user_id(self):
        self.assertEquals( 'test_user', self.openidauth.get_user_id( 'http://openid.lalala.ru/mail/test_user/' ) )

    def test_throws_on_empty(self):
        with self.assertRaises( Exception ):
            self.openidauth.get_user_id( 'http://openid.mail.ru/mail/' )

    def test_throws_on_invalid(self):
        with self.assertRaises( Exception ):
            self.openidauth.get_user_id( 'http://openid.asdfasdfasd/' )

