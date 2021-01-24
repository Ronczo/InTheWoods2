from django.urls import path
from .views import DisplayBooks, NewBook, EditBook, RateBook, DeleteBook, SortedBooks, OftenRate, Search

urlpatterns = [
    path('main', DisplayBooks.as_view(), name='main'),
    path('new_book', NewBook.as_view(), name='new_book'),
    path('edit_book/<int:pk>', EditBook.as_view(), name='edit_book'),
    path('edit_book/<int:pk>/delete', DeleteBook.as_view(), name='delete_book'),
    path('edit_book/<int:pk>/rate_book', RateBook.as_view(), name='rate_book'),
    path('sorted_books', SortedBooks.as_view(), name='sorted_books'),
    path('often_rate', OftenRate.as_view(), name='often_rated'),
    path('search', Search.as_view(), name='search'),
    path('searchbar', Search.as_view, name='searchbar')

]
