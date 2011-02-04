# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
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

@receiver(pre_save, sender=Post)
def preview_generator(sender, instance, **kwargs):
    words = instance.content.split(' ')[:20]
    instance.preview = ' '.join(words)

@receiver(pre_save, sender=Post)
def on_new_post(sender, instance, **kwargs):
    exist = len(Post.objects.filter( title=instance.title )) != 0
    if not exist:
        body = loader.get_template( 'email_new_post.txt' )
        subj = loader.get_template( 'email_new_post_subj.txt' )
        send_email_to_subscribers( u"У нас новая статья!", body.render( Context({'title':instance.title}) ) )
    else:
        logging.info( 'post changed, we are not going to send notification' )

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
            # try:
                logging.info( 'Sending "' + subject + '" to ' + subscriber.username + ' on ' + subscriber.email )
                send_email( subject, content, 'author@fromrussiatous.com', subscriber.email )
            # except Exception, e:
            #     logging.warning( 'Failed to send email to ' + subscriber.username + ' on ' + subscriber.email + ': ' + str(e) )
        
def send_email( subject, content, from_mail, to_mail ):
#    send_mail( subject, content, 'author@fromrussiatous.com', [subscriber.email] )
    msg = EmailMessage( subject, content, from_mail, [to_mail], 
                        headers = {'Reply-To': 'parshin.da@gmail.com'})
    import sys
    sys.stderr.write( msg.message() )
