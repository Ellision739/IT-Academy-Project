from django.db import models
from django.conf import settings

GENRE_CHOICES = [
    ('fantasy', 'Фэнтези'),
    ('sci-fi', 'Научная фантастика'),
    ('detective', 'Детектив'),
    ('classic', 'Классика'),
    ('romance', 'Романтика'),
    ('thriller', 'Триллер'),
    ('horror', 'Ужасы'),
    ('adventure', 'Приключения'),
    ('mystery', 'Мистика'),
    ('historical', 'Историческая литература'),
    ('biography', 'Биография'),
    ('autobiography', 'Автобиография'),
    ('poetry', 'Поэзия'),
    ('drama', 'Драма'),
    ('comedy', 'Комедия'),
    ('satire', 'Сатира'),
    ('dystopia', 'Антиутопия'),
    ('utopia', 'Утопия'),
    ('young-adult', 'Подростковая литература'),
    ('children', 'Детская литература'),
    ('non-fiction', 'Нон-фикшн'),
    ('self-help', 'Саморазвитие'),
    ('psychology', 'Психология'),
    ('philosophy', 'Философия'),
    ('science', 'Наука'),
    ('education', 'Образование'),
    ('business', 'Бизнес'),
    ('economics', 'Экономика'),
    ('politics', 'Политика'),
    ('religion', 'Религия'),
    ('travel', 'Путешествия'),
    ('cookbook', 'Кулинария'),
    ('art', 'Искусство'),
    ('health', 'Здоровье'),
    ('technology', 'Технологии'),
    ('programming', 'Программирование'),
]

STATUS_CHOICES = [
    ('excellent', 'Отлично'),
    ('good', 'Хорошо'),
    ('average', 'Среднее'),
    ('bad', 'Плохое'),
]

class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО автора")
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __init_subclass__(cls):
        return super().__init_subclass__()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    description = models.TextField(blank=True, verbose_name="Описание")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, verbose_name="Жанр")

    authors = models.ManyToManyField(Author, verbose_name="Авторы", related_name="books")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    inventory_number = models.AutoField(primary_key=True, verbose_name="Инвентарный_номер")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Состояние")
    location = models.CharField(max_length=100, verbose_name="Место_хранения")

    class Meta:
        verbose_name = "Экземпляр"
        verbose_name_plural = "Экземпляры"

    def __str__(self):
        return f"№ {self.inventory_number} — {self.book.title}"

class Loan(models.Model):
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Читатель")
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE, verbose_name="Экземпляр книги")
    return_date = models.DateField(verbose_name="Срок_возврата")

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"

    def __str__(self):
        return f"{self.reader.username} — {self.book_instance.book.title}"
