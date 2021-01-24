from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=64, blank=False, unique=True)
    author = models.CharField(max_length=64, blank=False)
    year_of_release = models.DateField(default="2021-01-01")

    def __str__(self):
        return f"{self.title} written by {self.author} ({self.year_of_release})"

    def get_average_rate(self):
        rates = [rate for rate in Rate.objects.filter(rated_book=self)]
        result = 0
        try:
            for rate in rates:
                result += rate.stars
            return result / len(rates)
        except ZeroDivisionError as e:
            return 0

    def get_amount_rates(self):
        rates = [rate for rate in Rate.objects.filter(rated_book=self)]
        return len(rates)

    @staticmethod
    def sorted_list():
        books = Book.objects.all()
        new_list = sorted(books, key=lambda x: x.get_average_rate(), reverse=True)
        return new_list

    @staticmethod
    def sorted_by_amount_of_rates():
        books = Book.objects.all()
        new_list = sorted(books, key=lambda x: x.get_amount_rates(), reverse=True)
        return new_list

    @staticmethod
    def search_item(searching):
        books = Book.objects.all()
        list_of_possibility = []
        for book in books:
            if searching.lower() in book.title.lower() or searching.lower() in book.author.lower():
                list_of_possibility.append(book)
        return list_of_possibility


class Rate(models.Model):
    rates = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    stars = models.PositiveSmallIntegerField(default=3, choices=rates)
    rated_book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rate: {self.stars} ({self.rated_book})"
