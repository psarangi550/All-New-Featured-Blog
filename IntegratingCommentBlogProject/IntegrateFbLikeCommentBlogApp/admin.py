from django.contrib import admin
from .models import User,Blog,Comment
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=["id","author","published_date","blog_img","title","desc"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=["comment_body","comment_date"]
