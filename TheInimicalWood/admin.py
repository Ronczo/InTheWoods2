from django.contrib import admin
from .models import Hero, Item, Character



@admin.register(Character)
class Character_admin_view(admin.ModelAdmin):
    fields = ['name', 'hero_class', 'playable', 'belongs_to']
    # list_display = ['name', 'hero_class']
    list_filter = ['hero_class']
    search_fields = ['name']


admin.site.register(Hero)
admin.site.register(Item)

# Register your models here.
