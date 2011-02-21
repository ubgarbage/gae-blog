from django.conf.urls.defaults import *
from models import *
import views

urlpatterns = patterns('',
    (r"^$", views.forum_view),
    (r"^thread/(\d+)/$", views.thread_view),
    (r"^post/(new_thread|reply)/(\d+)/$", views.post),
    (r"^reply/(\d+)/$", views.reply),
#    (r"^profile/(\d+)/$", views.profile),
    (r"^new_thread/$", views.new_thread),
)
