from django.urls import path
from. views import home, game, create_character, overview, specialthanks, delete_character


urlpatterns = [
    path('', home, name='home'),
    path('game/', game, name='game'),
    path('create_character/', create_character, name='create_character'),
    path('overview/<int:id>', overview, name='overview'),
    path('specialthanks/', specialthanks, name='specialthanks'),
    path('delete/<int:id>', delete_character, name='delete')

]