from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from openid.consumer import consumer
from utils import get_view_url, get_base_url
from external_auth.utils import authenticate_without_pass
import r
e
class OpenIdAuthenticator:

    def __init__( self, url_head, url_tail ):
        self.url_head = url_head
        self.url_tail = url_tail

    def openid_login( self. request, user_id ):
        if( '' == user_id and request.method == 'POST' ):
            redirect_url = get_view_url( request, self.openid_login, args=[''] )
            redirect_url = redirect_url + request.POST['username']
            return HttpResponseRedirect( redirect_url )

        c = consumer.Consumer( request.session, None )
        auth_request = c.begin( self.url_head + user_id + self.url_tail )

        redirect_url = auth_request.redirectURL( realm=get_base_url(request), return_to=get_view_url(request, self.check_and_auth) )
        return HttpResponseRedirect( redirect_url )

    def check_and_auth(self, request):
        c = consumer.Consumer( request.session, None )

        params = {}
        if( request.method == 'POST' ):
            params = request.POST
        else:
            params = request.GET

        auth_response = c.complete( params, get_view_url(request, self.check_and_auth) )

        if consumer.SUCCESS == auth_response.status:
            user_id = get_user_id( auth_response.getDisplayIdentifier() )
            authenticate_without_pass( user_id, user_id + '@yandex.ru', request )
            return HttpResponseRedirect( '/' )

        return HttpResponse( 'Failed' )


def get_user_id( identifier ):
    match = re.match( r"http://openid.yandex.ru/(.*)/", identifier )

    if None == match.group(1) or "" == match.group(1):
        raise Exception( 'invalid id' )

    return match.group(1)
