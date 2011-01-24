from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from openid.consumer import consumer
from external_auth.auth_utils import authenticate_without_pass
import utils
import re

class OpenIdAuthenticator:

    def __init__( self, url_head, url_tail, domain ):
        self.url_head = url_head
        self.url_tail = url_tail
        self.domain = domain

    def openid_login( self, request, user_id ):
        if( '' == user_id and request.method == 'POST' ):
            redirect_url = utils.get_view_url( request, self.openid_login, args=[''] )
            redirect_url = redirect_url + request.POST['username']
            return HttpResponseRedirect( redirect_url )

        c = consumer.Consumer( request.session, None )
        auth_request = c.begin( self.url_head + user_id + self.url_tail )

        redirect_url = auth_request.redirectURL( realm=utils.get_base_url(request), return_to=utils.get_view_url(request, self.check_and_auth) )
        return HttpResponseRedirect( redirect_url )

    def check_and_auth(self, request):
        c = consumer.Consumer( request.session, None )

        params = {}
        if( request.method == 'POST' ):
            params = request.POST
        else:
            params = request.GET

        auth_response = c.complete( params, utils.get_view_url(request, self.check_and_auth) )

        if consumer.SUCCESS == auth_response.status:
            user_id = self.get_user_id( auth_response.getDisplayIdentifier() )
            authenticate_without_pass( user_id, user_id + '@' + self.domain, request )
            return HttpResponseRedirect( '/' )

        return HttpResponse( 'Failed' )

    def get_user_id( self, identifier ):
        match = re.match( self.url_head + r"(.*)" + self.url_tail, identifier )

        if None == match.group(1) or "" == match.group(1):
            raise Exception( 'invalid id' )

        return match.group(1)


