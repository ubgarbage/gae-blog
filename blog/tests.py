from django.test.client import Client
from django.test import TestCase
from models import Post, Subscriber
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from test_utils import AuthViews

class PostTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user( username="test", email="test@test.com", password="test" )
        self.user.save()

    def test_unicode_returns_post_title(self):
        post = Post.objects.create( title='test_title', content='test_content', author=self.user )
        self.assertEquals( 'test_title', str(post) )

    def test_preview_is_generated(self):
        post = Post( title='test preview', content='word1 word2', author=self.user )
        post.save()
        self.assertEquals( post.preview, 'word1 word2' )


class BlogViews(AuthViews):

    def test_ok_for_auth_users(self):
        self.get_response_check_ok()

class PostsViewTest(BlogViews, TestCase):

    def setUp(self):
        self.set_url('/blog/posts/')

    def test_user_see_posts_list(self):
        post1 = Post( title='test post', content='test post content', author=self.user )
        post1.save()
        post2 = Post( title='test post 2', content='test post content 2', author=self.user )
        post2.save()
        response = self.get_response()
        self.assertIn( post1, response.context['posts'] )
        self.assertIn( post2, response.context['posts'] )
       
class PostViewTest(BlogViews, TestCase):

    def setUp(self):
        self.client = Client( HTTP_HOST='test_host' )
        self.set_url('/blog/posts/post/')
        self.post = Post( title='test post', content='test post content', author=self.user )
        self.post.save()
        self.set_url_params( str(self.post.id) + '/' )

    def test_returns_post(self):
        response = self.get_response()
        self.assertEquals( self.post, response.context['post'] )
        
    def test_returns_404_on_notfound(self):
        self.set_url_params( '2222/' )
        response = self.get_response()
        self.assertEquals( 404, response.status_code )

class SubscribeViewTest(BlogViews, TestCase):
    
    def setUp(self):
        self.set_url('/blog/subscribe/')
        
    def test_subscribe_add_user(self):
        response = self.get_response_check_ok()
        #execute without exception
        Subscriber.objects.get( user=self.user )

    def test_subscribe_doesnt_add_if_exists(self):
        Subscriber.objects.create( user=self.user )
        response = self.get_response_check_ok()
        self.assertEquals( 1, len(Subscriber.objects.all()) )

class UnsubscribeViewTest(BlogViews, TestCase):
    
    def setUp(self):
        self.set_url('/blog/unsubscribe/')

    def test_unsubscribe_removes_user_from_subscribers(self):
        Subscriber.objects.create( user=self.user )
        response = self.get_response_check_ok()
        self.assertEquals( 0, len(Subscriber.objects.all()) )
        
    def test_unsubscribe_returns_ok_if_not_subscribed(self):
        response = self.get_response_check_ok()
