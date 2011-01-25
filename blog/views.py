from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
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
    comments = Comment.objects.order_by('-submit_date')[0:10]
    context = RequestContext( request, {'posts': posts, 'comments': comments} )
    return render_to_response( 'posts.html', context )

@login_required
def post(request, post_id):
    ret = redirect_to_last_comment(request)
    if None != ret:
        return ret

    post_obj = Post.objects.get( id=post_id )
    context = RequestContext( request, 
                              { 'post':post_obj, 
                                'username':request.user.username, 
                                'redirect_after_comment':get_view_url(request, post, [post_id]) } )
    context.update( csrf(request) )
    return render_to_response( 'post.html', context )


def redirect_to_last_comment(request):
    if 'c' in request.GET:
        try:
            comment = Comment.objects.get(pk=request.GET['c'])
            return redirect( comment.get_absolute_url() )
        except (ObjectDoesNotExist, ValueError):
            pass
