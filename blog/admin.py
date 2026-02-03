from django.contrib import admin
from .models import Category, Post, Comment

# Register Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

# Register Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)} if hasattr(Post, 'slug') else {}

# Register Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
