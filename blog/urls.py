from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.all_posts, name='all_posts'),
    path('stories/', views.stories_list, name='stories'),
    path('story/create/', views.create_story, name='create_story'),
    path('story/<int:pk>/', views.view_story, name='view_story'),
    path('story/<int:pk>/delete/', views.delete_story, name='delete_story'),
    path('story/<int:pk>/viewers/', views.story_viewers, name='story_viewers'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='blog/login.html'),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/update/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
]
