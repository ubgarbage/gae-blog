# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from utils import get_view_url
from models import Post

@login_required
def main(request):
    return redirect( 'posts/' )

@login_required
def posts(request):
    posts = Post.objects.all()
    return render_to_response( 'posts.html', {'posts': posts} )

@login_required
def post(request, post_id):
    post_obj = Post.objects.get( id=post_id )
    c = { 'post':post_obj, 'username':request.user.username, 'redirect_after_comment':get_view_url(request, post, [post_id]) }
    c.update( csrf(request) )
    return render_to_response( 'post.html', c )

