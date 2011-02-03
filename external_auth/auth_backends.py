from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import logging
from models import AllowedUser

class NoPassBackend( ModelBackend ):
    
    def check_if_allowed( self, name ):
        try:
            AllowedUser.objects.get( username=name )
        except AllowedUser.DoesNotExist:
            return False
        return True

    def get_or_create_user( self, name, email ):
        user = None
        try:
            user = User.objects.get( username=name )
        except User.DoesNotExist:
            user = User.objects.create_user( name, email )
            user.save()
            
        return user

    def authenticate( self, username=None, password=None, nopass=False, email='' ):
        logging.info( str(username) + ' requested auth with email: ' + str(email) )
        if nopass and username != None:
            username = username.lower()
            if self.check_if_allowed( username ):
                return self.get_or_create_user( username, email )
            else:
                logging.error( str(email) + ' requested login, but he is not in allowed list' )
                return None
        else:
            return None
