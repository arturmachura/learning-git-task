from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Author, Book, Borrow


def books_list(request):
    paginator = Paginator(Book.objects.all(), 5)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)
    return render(request, "books/books_list.html", {"books": books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        if book.is_on_shelf():
            Borrow.objects.create(book=book, user=request.user)
            messages.add_message(request, messages.SUCCESS, "Book borrowed!")
        else:
            messages.add_message(request, messages.ERROR, "This book is not on the shelf.")
        return redirect("books:book_details", pk=book.pk)

    return render(request, "books/book_details.html", {"book": book})


def authors_list(request):
    paginator = Paginator(Author.objects.all(), 5)
    page_number = request.GET.get("page")
    authors = paginator.get_page(page_number)
    return render(request, "books/authors_list.html", {"authors": authors})


def author_details(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, "books/author_details.html", {"author": author})


@login_required
def my_borrows(request):
    if request.method == "POST" and "borrow_id" in request.POST:
        borrow = get_object_or_404(
            Borrow, id=int(request.POST["borrow_id"]), user=request.user
        )
        borrow.is_returned = True
        borrow.returned_at = timezone.now()
        borrow.save()
        messages.add_message(request, messages.SUCCESS, "Book returned!")
        return redirect("books:my_borrows")

    borrows = Borrow.objects.filter(user=request.user)
    return render(request, "books/my_borrows.html", {"borrows": borrows})
