from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import Blog
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .forms import EmailSendForm
from django.conf import settings
from django.urls import reverse
from taggit.models import Tag
from django.db.models import Count
from .forms import CommentForm
from django.urls import reverse
# Createur views here.

#blog_list_view
def blog_list_view(request,tag_slug=None):
    blog_list=Blog.objects.all()
    if tag_slug==None:
        tag=None
    if tag_slug:
        tag=Tag.objects.get(slug=tag_slug)
        blog_list=Blog.objects.filter(tags__in=[tag])
    paginator=Paginator(blog_list,3)
    page_number=request.GET.get("page")
    pages=paginator.get_page(page_number)
    context={"pages":pages,'tags':tag,}
    return render(request, "IntegrateFbLikeCommentBlogApp/blog_list.html", context)

#blog_detail view
def blog_detail_view(request,id):
    blog=get_object_or_404(Blog,id=id)
    blog_tag_id=blog.tags.values_list("id",flat=True)
    all_blogs=Blog.objects.filter(tags__id__in=[blog_tag_id]).exclude(id=blog.id)
    similar_post=all_blogs.annotate(same_tags=Count("tags")).order_by('-same_tags','-published_date')[0:3]
    all_comments=blog.blog_comment.all()
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.blog=blog
            new_comment.user=request.user
            new_comment.save()
            return HttpResponseRedirect(reverse("blog_detail",kwargs={"id":blog.id}))
    form=CommentForm()
    context={"blog":blog,"similar_post":similar_post,"form":form,"comments":all_comments}
    return render(request, "IntegrateFbLikeCommentBlogApp/blog_detail.html",context)

#Email Send Form functionality
def EmailSendView(request,id):
    blog=get_object_or_404(Blog,id=id)
    sent=False
    if request.method == "POST":
        form=EmailSendForm(request.POST)
        if form.is_valid():
            to=form.cleaned_data["to"]
            sender=form.cleaned_data['name']
            comments=form.cleaned_data["comments"]
            url=str(request.build_absolute_uri(reverse("blog_detail",kwargs={"id":blog.id})))
            comment=f'{comments}\n\n{url}'
            subject=f'{sender}recomend you {blog.title}'
            send_mail(subject , comment , settings.EMAIL_HOST_USER , [to])
            sent=True
    else:
        form=EmailSendForm()
    return render(request, "IntegrateFbLikeCommentBlogApp/email_send.html", {"form":form,"blog":blog,"sent":sent})
