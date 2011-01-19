import django.conf.urls.defaults
import views

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( '^$', views.main ),
                        ( 'posts/$', views.posts ),
                        ( 'post/(\d+)/$', views.post ), )

