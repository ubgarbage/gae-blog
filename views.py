from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout

def main(request):
    return HttpResponseRedirect( '/blog/' )

def main_logout(request):
    logout(request)
    return HttpResponseRedirect( '/' )

