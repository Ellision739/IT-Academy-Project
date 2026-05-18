from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Book, BookInstance

User = get_user_model()


class LibraryLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testworker', password='password123')

        self.book1 = Book.objects.create(
            title='Тестирование Django',
            isbn='9785932861592',
            genre='programming'
        )
        self.book2 = Book.objects.create(
            title='Мастер и Маргарита',
            isbn='9785170878833',
            genre='classic'
        )

        self.instance = BookInstance.objects.create(
            book=self.book1,
            inventory_number=1001,
            status='available',
            location='Стойка тестов'
        )

    def test_available_copies_count(self):
        """Проверка корректности работы счетчика доступных книг"""
        self.assertEqual(self.book1.available_copies_count, 1)

    def test_reserved_copies_count(self):
        """Проверка, что забронированная книга пропадает из доступных"""
        self.instance.status = 'reserved'
        self.instance.save()
        self.assertEqual(self.book1.available_copies_count, 0)

    def test_book_search(self):
        """Тестирование работы поиска в каталоге книг"""
        url = reverse('book_list')

        response = self.client.get(url, {'search': 'Django'})
        self.assertContains(response, 'Тестирование Django')
        self.assertNotContains(response, 'Мастер и Маргарита')
