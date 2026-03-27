from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .admin import CommentAdmin, PostAdmin
from .models import Comment, Post


class AdminConfigTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(username='adminuser', password='secret123')
        self.post = Post.objects.create(
            title='Admin Post',
            content='Post content',
            author=self.user,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            body='This is a comment managed by admin.',
        )

    def test_post_admin_shows_key_fields(self):
        admin_obj = PostAdmin(Post, self.site)

        self.assertEqual(
            admin_obj.list_display,
            ('title', 'author', 'created_at', 'total_likes'),
        )

    def test_comment_admin_short_body(self):
        admin_obj = CommentAdmin(Comment, self.site)

        self.assertEqual(admin_obj.short_body(self.comment), self.comment.body)


class PostPermissionTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='secret123')
        self.other_user = User.objects.create_user(username='other', password='secret123')
        self.admin_user = User.objects.create_superuser(
            username='siteadmin',
            email='admin@example.com',
            password='secret123',
        )
        self.post = Post.objects.create(
            title='Protected Post',
            content='Original content',
            author=self.author,
        )

    def test_superuser_can_update_another_users_post(self):
        self.client.login(username='siteadmin', password='secret123')

        response = self.client.post(
            reverse('post_update', args=[self.post.pk]),
            {
                'title': 'Updated by Admin',
                'content': 'Updated content',
            },
        )

        self.assertRedirects(response, reverse('post_detail', args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated by Admin')

    def test_superuser_can_delete_another_users_post(self):
        self.client.login(username='siteadmin', password='secret123')

        response = self.client.get(reverse('post_delete', args=[self.post.pk]))

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_regular_user_cannot_update_another_users_post(self):
        self.client.login(username='other', password='secret123')

        response = self.client.post(
            reverse('post_update', args=[self.post.pk]),
            {
                'title': 'Blocked update',
                'content': 'Blocked content',
            },
        )

        self.assertRedirects(response, reverse('home'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Protected Post')


class PostDetailTests(TestCase):
    def test_post_detail_shows_uploaded_image(self):
        user = User.objects.create_user(username='imageuser', password='secret123')
        image_file = SimpleUploadedFile(
            'post.jpg',
            (
                b'GIF87a\x01\x00\x01\x00\x80\x00\x00'
                b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
            ),
            content_type='image/gif',
        )
        post = Post.objects.create(
            title='Image Post',
            content='Post with image',
            author=user,
            image=image_file,
        )

        response = self.client.get(reverse('post_detail', args=[post.pk]))

        self.assertContains(response, post.image.url)
