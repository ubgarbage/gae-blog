import django.conf.urls.defaults
import views

urlpatterns = django.conf.urls.defaults.patterns( '',
                                                  ( 'delete/(\d+)/$', views.delete ), )



