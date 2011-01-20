from django.http import HttpResponse
import urlparse
import httplib

def testdebug1(request):
#     url = 'http://www.yahoo.com'

#     parsed = urlparse.urlparse(url)
#     protocol, host, path, parameters, query, fragment = parsed

#     adjusted_headers = {
#         'User-Agent':
#             'AppEngine-Google; (+http://code.google.com/appengine)',
#         'Host': host,
#         'Accept-Encoding': 'gzip',
#         }

# #DEBUG    2011-01-19 22:36:26,431 urlfetch_stub.py:200] Making HTTP request: host = openid.mail.ru, url = http://openid.mail.ru/mail/parshin_da, payload = None, headers = {'Host': 'openid.mail.ru', 'Connection': 'close', 'Accept-Encoding': 'gzip', 'Accept': 'text/html; q=0.3, application/xhtml+xml; q=0.5, application/xrds+xml', 'User-Agent': 'python-openid/2.2.1 (linux2) Python-urllib/2.6 AppEngine-Google; (+http://code.google.com/appengine)'}

#     connection = httplib.HTTPConnection(host)
#     connection.request('POST', path, None, adjusted_headers)
#     http_response = connection.getresponse()
#     http_response_data = http_response.read()
#     connection.close()
#     if http_response.getheader('content-encoding') == 'gzip':
#         gzip_stream = StringIO.StringIO(http_response_data)
#         gzip_file = gzip.GzipFile(fileobj=gzip_stream)
#         http_response_data = gzip_file.read()
          
    return HttpResponse( 'Hey' )
