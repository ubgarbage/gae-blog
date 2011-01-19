from django.http import HttpResponse, HttpResponseRedirect

def main(request):
    return HttpResponseRedirect( '/blog/' )
