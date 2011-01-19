from django.db import models

class AllowedUser(models.Model):
    username = models.CharField( max_length=255 )

    def __unicode__(self):
        return self.username

