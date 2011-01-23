from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Post(models.Model):
    title = models.CharField( max_length=255 )
    content = models.TextField()
    preview = models.TextField(blank=True)
    create_time = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']

@receiver(pre_save, sender=Post)
def preview_generator(sender, instance, **kwargs):
    words = instance.content.split(' ')[:20]
    instance.preview = ' '.join(words)
