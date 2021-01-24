from django.contrib import admin
from .models import Book, Rate

admin.site.register(Book)
admin.site.register(Rate)


class BookAdminView(admin.ModelAdmin):
    fields = ['title', 'author', 'year_of_release']


class RateAdminView(admin.ModelAdmin):
    fields = ['stars', 'rated_book']
