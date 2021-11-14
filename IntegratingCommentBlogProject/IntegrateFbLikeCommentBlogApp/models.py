from django.db import models
from django.contrib.auth.models import User #importing th user model here
from taggit.managers import TaggableManager
# Create your models here.

class Blog(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    published_date=models.DateTimeField(auto_now_add=True)
    blog_img=models.ImageField(upload_to="media", blank=True, null=True)
    title=models.CharField(max_length=200)
    desc=models.TextField()
    tags=TaggableManager()

    def __str__(self):
        return self.title

class Comment(models.Model):#creating the Comments model
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="blog_comment")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_comment")
    comment_body=models.TextField()
    comment_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment_body} comment on {self.blog}'




