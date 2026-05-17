from django.shortcuts import render
from .models import Book, Author, BookInstance
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Loan


def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
    }

    return render(request, 'catalog/index.html', context=context)

def book_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        books = Book.objects.filter(
            Q(title__iregex=search_query) |
            Q(genre__iregex=search_query) |
            Q(authors__name__iregex=search_query)
        ).distinct()
    else:
        books = Book.objects.all()

    context = {
        'books': books,
        'search_query': search_query,
    }
    return render(request, 'catalog/book_list.html', context)


@login_required
def my_books(request):
    user_loans = Loan.objects.filter(reader=request.user)

    return render(request, 'catalog/my_books.html', {'user_loans': user_loans})
