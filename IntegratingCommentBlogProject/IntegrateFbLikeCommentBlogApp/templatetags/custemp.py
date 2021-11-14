import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IntegratingCommentBlogProject.settings')
import django
django.setup()
from django import template
from IntegrateFbLikeCommentBlogApp.models import Blog,Comment
from IntegrateFbLikeCommentBlogApp.views import *
from django.db.models import Count,Max,Min
register = template.Library()
@register.inclusion_tag("IntegrateFbLikeCommentBlogApp/comment.html")
def comment_count():
    # for blog in Blog.objects.all():
      # comment_num=blog.blog_comment.order
    # counts=Blog.objects.all().annotate(Count("blog_comment__id"))[0:3]
    counts=Blog.objects.annotate(total_counts=Count('blog_comment__id')).order_by("-total_counts")[0:3]
    return {"counts":counts}

@register.inclusion_tag("IntegrateFbLikeCommentBlogApp/inclusion.html")
def latest_post():
    blog_list=Blog.objects.order_by("-published_date")[0:3]
    # for blog in Blog.objects.all():
        # max_comment=max(blog.blog_comment)
    return {"blogs":blog_list}


@register.simple_tag(name="less_comment")
def comment_less(count=3):
    less_counts=Blog.objects.all().annotate(total_counts=Count("blog_comment__id")).order_by('total_counts')[0:count]
    return less_counts

