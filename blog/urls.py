import django.conf.urls.defaults
import views

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( '^$', views.main ),
                        ( '^subscribe/$', views.subscribe ),
                        ( '^unsubscribe/$', views.unsubscribe ),
                        ( '^posts/$', views.posts ),
                        ( '^posts/post/(\d+)/$', views.post ), )

