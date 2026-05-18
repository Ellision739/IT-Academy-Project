from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('mybooks/', views.my_books, name='my_books'),
    path('register/', views.register, name='register'),
    path('order/<int:book_id>/', views.order_book, name='order_book'),
    path('cancel/<int:loan_id>/', views.cancel_order, name='cancel_order'),
]
