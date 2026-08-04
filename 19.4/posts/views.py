from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, PostForm
from .models import Author, Post


def posts_list(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Post created!")
            return redirect("posts:posts_list")
        messages.add_message(request, messages.ERROR, "Please fix the errors below.")
    else:
        form = PostForm()

    paginator = Paginator(Post.objects.all(), 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="posts/posts_list.html",
        context={"posts": posts, "form": form},
    )


def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(
        request=request,
        template_name="posts/post_details.html",
        context={"post": post},
    )


def authors_list(request):
    if request.method == "POST":
        form = AuthorForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Author created!")
            return redirect("posts:authors_list")
        messages.add_message(request, messages.ERROR, "Please fix the errors below.")
    else:
        form = AuthorForm()

    authors = Author.objects.all()
    return render(
        request=request,
        template_name="posts/authors_list.html",
        context={"authors": authors, "form": form},
    )


def author_details(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(
        request=request,
        template_name="posts/author_details.html",
        context={"author": author},
    )
