from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from utils import get_view_url
from models import Post, Subscriber
from forum.models import ForumPost
import logging


@login_required
def main(request):
    return redirect( 'posts/' )


class ViewCreator(type):

    @method_decorator(login_required)
    def __call__(cls, request, *args, **kwargs):
        instance = super(ViewCreator, cls).__call__(request)
        return instance.render(*args, **kwargs)

class BlogBaseView:
    
    __metaclass__ = ViewCreator

    def __init__(self, request):
        self.Request = request
        self.Context = RequestContext( request )
        self.User = self.Request.user

    def update_context(self):
        self.add_comments( self.Context )
        self.add_is_subscriber_flag()        

    def add_comments(self, context):
        comments = Comment.objects.order_by('-submit_date')[0:5]
        context['comments'] = comments
        forum_posts = ForumPost.objects.order_by('-created')[0:5]
        context['forum_posts'] = forum_posts
        return context

    def add_is_subscriber_flag(self):
        self.Context['is_subscribed']=is_subscriber(self.User)

    def render_template(self, template_name):
        self.update_context()
        return render_to_response( template_name, self.Context )

class PostView(BlogBaseView):
    
    def render(self, post_id, *args):
        ret = self.redirect_to_last_comment(self.Request)
        if None != ret:
            return ret

        post_obj = get_object_or_404( Post, id=post_id )
        self.Context['post'] = post_obj;
        self.Context['redirect_after_comment'] = get_view_url(self.Request, PostView, [post_id])
        self.Context.update( csrf(self.Request) )
        logging.info( "User " + self.Request.user.username + ": rendering post '" + post_obj.title + "'" ) 
        return self.render_template( 'post.html' )

    def redirect_to_last_comment(self, request):
        if 'c' in request.GET:
            try:
                comment = Comment.objects.get(pk=request.GET['c'])
                return redirect( comment.get_absolute_url() )
            except (ObjectDoesNotExist, ValueError):
                pass

class PostsView(BlogBaseView):

    def render(self, *args):
        posts = Post.objects.all()
        self.Context['posts'] = posts
        logging.info( "User " + self.Request.user.username + ": rendering posts list" ) 
        return self.render_template( 'posts.html' )

class SubscribeView(BlogBaseView):

    def render(self, *args):
        if is_subscriber(self.User):
            subscriber = Subscriber.objects.get( user=self.User )
            return self.render_template( 'subscribe_already.html' )
        else:
            logging.info( 'Subscribing ' + self.User.username )
            subscriber = Subscriber.objects.create( user=self.User )
            subscriber.save()
        return self.render_template( 'subscribed.html' )


class UnsubscribeView(BlogBaseView):

    def render(self, *args):
        if is_subscriber(self.User):
            subscriber = Subscriber.objects.get( user=self.User )
            logging.info( 'Unsubscribing ' + self.User.username )
            subscriber.delete()
            return self.render_template( 'subscribe_un.html' )
        else:
            return self.render_template( 'subscribe_un_notsubscribed.html' )

def is_subscriber(user):
    return False if 0 == len(Subscriber.objects.filter( user=user )) else True
