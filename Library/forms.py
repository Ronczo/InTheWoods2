from django.forms import ModelForm
from .models import Book, Rate


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year_of_release']


class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['stars']
