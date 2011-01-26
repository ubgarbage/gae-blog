from django.test.client import Client
from django.test import TestCase
from models import Post
from views import posts
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from test_utils import AuthViews

class PostTest(TestCase):
    def test_unicode_returns_post_title(self):
        post = Post.objects.create( title='test_title', content='test_content' )
        self.assertEquals( 'test_title', str(post) )

    def test_preview_is_generated(self):
        post = Post( title='test preview', content='word1 word2' )
        post.save()
        self.assertEquals( post.preview, 'word1 word2' )


class BlogViews(AuthViews):

    def test_ok_for_auth_users(self):
        response = self.get_response()
        self.assertEquals( response.status_code, 200 )


class PostsView(BlogViews, TestCase):

    def setUp(self):
        self.set_url('/blog/posts/')

    def test_user_see_posts_list(self):
        post1 = Post( title='test post', content='test post content' )
        post1.save()
        post2 = Post( title='test post 2', content='test post content 2' )
        post2.save()
        response = self.get_response()
        self.assertIn( post1, response.context['posts'] )
        self.assertIn( post2, response.context['posts'] )
       
class PostView(BlogViews, TestCase):

    def setUp(self):
        self.client = Client( HTTP_HOST='test_host' )
        self.set_url('/blog/post/')
        self.post = Post( title='test post', content='test post content' )
        self.post.save()
        self.set_url_params( str(self.post.id) + '/' )

    def test_returns_post(self):
        response = self.get_response()
        self.assertEquals( self.post, response.context['post'] )
        
    def test_returns_404_on_notfound(self):
        self.set_url_params( '2222/' )
        response = self.get_response()
        self.assertEquals( 404, response.status_code )
