from django.contrib import admin

from .models import Comment, Post, Story


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'total_likes')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_body', 'user', 'post', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('body', 'user__username', 'post__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    @admin.display(description='Comment')
    def short_body(self, obj):
        return obj.body[:60] + ('...' if len(obj.body) > 60 else '')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_views')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
