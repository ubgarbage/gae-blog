from django.test.client import Client
from django.test import TestCase
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from blog.models import Post
from test_utils import AuthViews
from django.contrib.contenttypes.models import ContentType
import settings
import logging

class DeleteCommentView(AuthViews, TestCase):

    def setUpComment(self):
        self.c1 = Comment.objects.create(
            content_type = ContentType.objects.get_for_model(Post),
            object_pk = "1",
            user = self.user,
            user_name = "somebody",
            user_email = "test@test.com",
            user_url = "",
            comment = "test comment",
            site = Site.objects.get_current(), )
        self.c1.save()

    def setUp(self):
        site = Site( id=settings.SITE_ID, domain = "example.com", name = "test" )
        site.save()
        self.set_url('/comment/delete/')
        self.set_url_params( '123/' )
        self.setUpComment()

    def test_redirect_to_next_for_auth_users(self):
        self.set_url_params( '222/?next=/test/location' )
        response = self.get_response()
        self.assertEquals( response.status_code, 302 )
        self.assertIn( 'test/location', response['Location'] )

    def test_delete_comment(self):
        self.set_url_params( str(self.c1.pk) + '/' )
        response = self.get_response()
        self.assertEquals( 302, response.status_code )
        self.assertTrue( Comment.objects.get( pk=self.c1.pk ).is_removed )

    def test_staff_can_delete_others_comment(self):
        self.set_url_params( str(self.c1.pk) + '/' )
        response = self.get_response_for_staff()

        self.assertEquals( 302, response.status_code )
        self.assertTrue( Comment.objects.get( pk=self.c1.pk ).is_removed )
        
