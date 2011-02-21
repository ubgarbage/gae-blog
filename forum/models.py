from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save


class Thread(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

    def num_posts(self):
        return self.forumpost_set.count()

    def num_replies(self):
        return self.forumpost_set.count() - 1

    def last_post(self):
        if self.forumpost_set.count():
            return self.forumpost_set.order_by("created")[0]


class ForumPost(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length=10000)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.thread, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True

    # def profile_data(self):
    #     p = self.creator.userprofile_set.all()[0]
    #     return p.posts, p.avatar


# class UserProfile(models.Model):
#     avatar = models.ImageField("Profile Pic", upload_to="images/", blank=True, null=True)
#     posts = models.IntegerField(default=0)
#     user = models.ForeignKey(User, unique=True)

#     def __unicode__(self):
#         return unicode(self.user)


### Admin

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["user"]

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created"]
    list_filter = ["creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "thread", "creator", "created"]


# def create_user_profile(sender, **kwargs):
#     """When creating a new user, make a profile for him."""
#     u = kwargs["instance"]
#     if not UserProfile.objects.filter(user=u):
#         UserProfile(user=u).save()

# post_save.connect(create_user_profile, sender=User)

