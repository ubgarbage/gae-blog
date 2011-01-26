from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from utils import get_view_url
from models import Post

@login_required
def main(request):
    return redirect( 'posts/' )

@login_required
def posts(request):
    posts = Post.objects.all()
    context = RequestContext( request, {'posts': posts} )
    add_comments( context )
    return render_to_response( 'posts.html', context )

def add_comments( context ):
    comments = Comment.objects.order_by('-submit_date')[0:10]
    context['comments'] = comments

@login_required
def post(request, post_id):
    ret = redirect_to_last_comment(request)
    if None != ret:
        return ret

    post_obj = get_object_or_404( Post, id=post_id )
    context = RequestContext( request, 
                              { 'post':post_obj, 
                                'redirect_after_comment':get_view_url(request, post, [post_id]) } )
    context.update( csrf(request) )
    add_comments( context )
    return render_to_response( 'post.html', context )


def redirect_to_last_comment(request):
    if 'c' in request.GET:
        try:
            comment = Comment.objects.get(pk=request.GET['c'])
            return redirect( comment.get_absolute_url() )
        except (ObjectDoesNotExist, ValueError):
            pass
