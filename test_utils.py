from django.test.client import Client
from django.contrib.auth.models import User
import logging

class AuthViews():

    def setUpUsers(self):
        self.user = User.objects.create_user( username="test", email="test@test.com", password="test" )
        self.user.save()
        self.staff_user = User.objects.create_user( username="test_staff", email="test_staff@test.com", password="test" )
        self.staff_user.is_staff = True
        self.staff_user.save()
    
    def set_url(self, url):
        self.url = url
        self.url_params = ''
        self.setUpUsers()

    def set_url_params( self, url_params ):
        self.url_params = url_params

    def login(self, user):
        self.client.login( username=user.username, password='test' )
        
    def get_anonym_response( self ):
        return self.client.get( self.url + self.url_params )

    def get_response( self ):
        self.login( self.user )
        return self.client.get( self.url + self.url_params )

    def get_response_for_staff( self ):
        self.login( self.staff_user )
        return self.client.get( self.url + self.url_params )

    def get_response_check_ok( self ):
        response = self.get_response()
        self.assertEquals( 200, response.status_code )
        return response

    def test_redirect_for_nonauth_users( self ):
        response = self.get_anonym_response()
        self.assertEquals( response.status_code, 302 )
        self.assertIn( 'accounts/login', response['Location'] )
        
       
