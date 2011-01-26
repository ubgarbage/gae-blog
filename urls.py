from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login
import views
import blog.urls
import external_auth.urls
import comment.urls
import testdebug.views

admin.autodiscover()

urlpatterns = patterns( '', 
                        ( '^$', views.main ),
                        ( '^admin/', include(admin.site.urls) ),
                        ( '^accounts/login/$', login, { 'template_name' : 'login.html' } ),
                        ( '^logout/$', views.main_logout ),
                        ( '^accounts/external/', include(external_auth.urls) ),
                        ( r'^comments/', include('django.contrib.comments.urls') ),
                        ( '^comment/', include(comment.urls) ),
                        ( '^blog/', include(blog.urls) ),
                        ( '^testdebug/', testdebug.views.testdebug1 ), )


