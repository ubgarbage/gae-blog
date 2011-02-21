
from models import *
from django.contrib import admin

admin.site.register(Thread, ThreadAdmin)
admin.site.register(ForumPost, PostAdmin)
admin.site.register(UserProfile, ProfileAdmin)
