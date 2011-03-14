# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.template import loader, Context
import logging

class Post(models.Model):
    title = models.CharField( max_length=255 )
    content = models.TextField()
    preview = models.TextField(blank=True)
    create_time = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']

    def get_absolute_url(self):
        return '/blog/posts/post/' + str(self.id)

    def save(self, *args, **kwargs):
        notify=False
        if not self.pk:
            notify=True
        super(Post, self).save(args, kwargs)
        if notify:
            notify_subscribers( self )
        else:
            logging.info( 'post changed, we are not going to send notification' )

def notify_subscribers(instance):
    body = loader.get_template( 'email_new_post.txt' )
    subj = loader.get_template( 'email_new_post_subj.txt' )
    send_email_to_subscribers( subj.render( Context({'post':instance}) ), body.render( Context({'post':instance}) ) )

@receiver(pre_save, sender=Post)
def preview_generator(sender, instance, **kwargs):
    words = instance.content.split(' ')[:20]
    instance.preview = ' '.join(words)

class Subscriber(models.Model):
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return self.user.username

def get_subscriber( subuser ):
    try:
        return Subscriber.objects.get(user=subuser)
    except Subscriber.DoesNotExist:
        return None

def send_email_to_subscribers( subject, content ):
    for subscriber in User.objects.all():
        if None != get_subscriber( subscriber ):
            try:
                logging.info( 'Sending "' + subject + '" to ' + subscriber.username + ' on ' + subscriber.email )
                send_mail( subject, content, 'parshin.da@gmail.com', [subscriber.email] )
            except Exception, e:
                logging.warning( 'Failed to send email to ' + subscriber.username + ' on ' + subscriber.email + ': ' + str(e) )
        
