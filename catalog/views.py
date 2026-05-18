from django.shortcuts import render
from .models import Book, Author, BookInstance
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Loan
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta


User = get_user_model()


class CustomRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


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
            Q(title__iregex=search_query) | Q(genre__iregex=search_query) | Q(authors__name__iregex=search_query)
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


@login_required
def order_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)

        already_has_it = Loan.objects.filter(
            reader=request.user,
            book_instance__book=book
        ).exists()

        if already_has_it:
            return redirect('my_books')

        instance = BookInstance.objects.filter(book=book, status='available').first()

        if instance:
            instance.status = 'reserved'
            instance.save()

            Loan.objects.create(
                reader=request.user,
                book_instance=instance,
                return_date=date.today() + timedelta(days=14)
            )

    return redirect('my_books')


@login_required
def cancel_order(request, loan_id):
    if request.method == 'POST':
        loan = get_object_or_404(Loan, id=loan_id, reader=request.user)
        instance = loan.book_instance

        instance.status = 'available'
        instance.save()

        loan.delete()

    return redirect('my_books')
