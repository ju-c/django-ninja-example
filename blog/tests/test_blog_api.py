from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from datetime import datetime

from blog.models import Post


class BlogApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com'
        )
        self.user1 = User.objects.create_user(
            username='test1',
            password='12test12',
            email='test1@example.com'
        )
        self.blogpost = Post.objects.create(
            author=self.user,
            title='This is a blog post title',
            body='This is a blog post body',
            created_on=datetime.now()
        )
        self.blogpost_hello = {
            'title': 'Hello there!',
            'body': 'This is a body content'
        }
        self.blogpost_update = {
            'title': 'This is an edited blog post title',
            'body': 'This is an edited blog post body'
        }

    def test_create_new_blog_post(self):
        """
        An authenticated user can create a new blog post.
        """
        self.client.force_login(self.user)
        url = reverse('blog_api:create_blog_post')
        response = self.client.post(url, data=self.blogpost_hello, content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_blog_posts_list(self):
        """
        Getting the blog posts list:
        """
        url = reverse('blog_api:list_blog_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['title'], self.blogpost.title)
        self.assertEqual(response.json()[0]['body'], self.blogpost.body)

    def test_get_single_blog_post(self):
        """
        Getting a single blog post.
        """
        url = reverse('blog_api:blog_post', kwargs={'blog_post_id': self.blogpost.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], self.blogpost.title)
        self.assertEqual(response.json()['body'], self.blogpost.body)

    def test_update_blog_post(self):
        """
        A user can only edit his/her own blog's post.
        """
        self.client.force_login(self.user)
        url = reverse('blog_api:blog_post', kwargs={'blog_post_id': self.blogpost.id})
        response = self.client.put(url, data=self.blogpost_update, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], self.blogpost_update['title'])
        self.assertEqual(response.json()['body'], self.blogpost_update['body'])

    def test_update_blog_post_without_permission(self):
        """
        Return a 404 error if a user try to update a post of which he/she is not the author.
        """
        self.client.force_login(self.user1)
        url = reverse('blog_api:blog_post', kwargs={'blog_post_id': self.blogpost.id})
        response = self.client.put(url, data=self.blogpost_update, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_blog_post(self):
        """
        A user can only delete his/her own blog's post.
        """
        self.client.force_login(self.user)
        url = reverse('blog_api:blog_post', kwargs={'blog_post_id': self.blogpost.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Blog post successfully deleted'], True)

    def test_delete_blog_post_without_permission(self):
        """
        Return a 404 error if a user try to delete a post of which he/she is not the author.
        """
        self.client.force_login(self.user1)
        url = reverse('blog_api:blog_post', kwargs={'blog_post_id': self.blogpost.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
