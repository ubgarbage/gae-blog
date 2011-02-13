import django.conf.urls.defaults
import views

urlpatterns = django.conf.urls.defaults.patterns( '',
                        ( '^$', views.main ),
                        ( '^subscribe/$', views.SubscribeView ),
                        ( '^unsubscribe/$', views.UnsubscribeView ),
                        ( '^posts/$', views.PostsView ),
                        ( '^posts/post/(\d+)/$', views.PostView ), )

