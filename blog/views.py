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
        self.add_comments( self.Context )
        self.add_is_subscriber_flag()

    def add_comments(self, context):
        comments = Comment.objects.order_by('-submit_date')[0:10]
        context['comments'] = comments
        return context

    def add_is_subscriber_flag(self):
        self.Context['is_subscriber']=is_subscriber(self.User)

class PostView(BlogBaseView):
    
    def render(self, post_id, *args):
        ret = self.redirect_to_last_comment(self.Request)
        if None != ret:
            return ret

        post_obj = get_object_or_404( Post, id=post_id )
        self.Context['post'] = post_obj;
        self.Context['redirect_after_comment'] = get_view_url(self.Request, PostView, [post_id])
        self.Context.update( csrf(self.Request) )
        return render_to_response( 'post.html', self.Context )

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
        return render_to_response( 'posts.html', self.Context )

class SubscribeView(BlogBaseView):

    def render(self, *args):
        if is_subscriber(self.User):
            subscriber = Subscriber.objects.get( user=self.User )
            return render_to_response( 'subscribe_already.html', self.Context )
        else:
            logging.info( 'Subscribing ' + self.User.username )
            subscriber = Subscriber.objects.create( user=self.User )
            subscriber.save()
        return render_to_response( 'subscribed.html', self.Context )


class UnsubscribeView(BlogBaseView):

    def render(self, *args):
        if is_subscriber(self.User):
            subscriber = Subscriber.objects.get( user=self.User )
            logging.info( 'Unsubscribing ' + self.User.username )
            subscriber.delete()
            return render_to_response( 'subscribe_un.html', self.Context )
        else:
            return render_to_response( 'subscribe_un_notsubscribed.html', self.Context )


def is_subscriber(user):
    return False if 0 == len(Subscriber.objects.filter( user=user )) else True
