from django.urls import path
from. views import home, game, create_character, Overview, specialthanks, delete_character, Shop, mission_select,\
    briefing, Combat, guest_book_new, guest_book
from . import combat


urlpatterns = [
    path('', home, name='home'),
    path('game/', game, name='game'),
    path('create_character/', create_character, name='create_character'),
    path('overview/<int:id>', Overview.as_view(), name='overview'),
    path('specialthanks/', specialthanks, name='specialthanks'),
    path('delete/<int:id>', delete_character, name='delete'),
    path('shop/<int:id>', Shop.as_view(), name='shop'),
    path('mission/<int:id>', mission_select, name="mission_select"),
    path('briefing<int:selected_mission>/<int:id>', briefing, name="briefing"),
    path('mission<int:selected_mission>/<int:id>/', Combat.as_view(), name="mission"),
    path('guest_book_new/', guest_book_new, name="guest_book_new"),
    path('guest_book/', guest_book, name="guest_book"),
]