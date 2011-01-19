from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
import views
import blog.urls
import external_auth.urls

admin.autodiscover()

urlpatterns = patterns( '', 
                        ( '^$', views.main ),
                        ( '^admin/', include(admin.site.urls) ),
                        ( '^accounts/login/$', login, { 'template_name' : 'login.html' } ),
                        ( '^accounts/logout/$', logout ),
                        ( '^accounts/external/', include(external_auth.urls) ),
                        ( r'^comments/', include('django.contrib.comments.urls') ),
                        ( '^blog/', include(blog.urls) ), )


