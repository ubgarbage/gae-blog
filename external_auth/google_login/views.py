from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from external_auth.auth_utils import authenticate_without_pass
from utils import get_view_url
import django
import urllib2
import urllib

def google_login(request):
    return_to = get_view_url( request, check_and_auth )
    return HttpResponseRedirect( 'https://www.google.com/accounts/o8/ud?openid.return_to=' + return_to + '&openid.ns.ax=http://openid.net/srv/ax/1.0&openid.ax.mode=fetch_request&openid.ax.required=email&openid.ax.type.email=http://schema.openid.net/contact/email&openid.mode=checkid_setup&openid.ns=http://specs.openid.net/auth/2.0&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select' )

def check_and_auth(request):
    params = {}
    if( request.method == 'POST' ):
        params = request.POST
    else:
        params = request.GET

    checker = GoogleAuthChecker( params, 'https://www.google.com/accounts/o8/ud' )
    if checker.check():
        (name, email) = get_username( params )
        authenticate_without_pass( name, email, request )
        return HttpResponseRedirect( '/' )
    else:
        return HttpResponse( 'Failed' )


def get_username( params ):
    email = params['openid.ext1.value.email']
    (name, rest) = email.split('@')
    return (name, email)

class GoogleAuthChecker:

    def __init__( self, params_readonly, check_uri = 'https://www.google.com/accounts/o8/ud' ):
        self.params = params_readonly.copy()
        self.check_uri = check_uri

    def get_url_for_check( self, url_base ):
        url = url_base + '?'
        for k,v in self.params.iteritems():
            url = url + urllib.quote(k) + '=' + urllib.quote(v) + '&'
            
        url = url[:len(url)-1]
        return url

    def check_response( self, response ):
        for line in response:
            if 0 == len(line):
                continue
            (name, value) = line.strip().split(':', 1)
            if "is_valid" == name and "true" == value:
                return True

        return False

    def check( self ):
        self.params['openid.mode'] = 'check_authentication'
        url = self.get_url_for_check( self.check_uri )
        data = urllib2.urlopen( url ).readlines()
        return self.check_response(data)
