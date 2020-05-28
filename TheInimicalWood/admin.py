from django.contrib import admin
from .models import Item, Character



@admin.register(Character)
class Character_admin_view(admin.ModelAdmin):
    fields = ['name', 'hero_class', 'belongs_to', 'attack_dmg', 'defence', 'hp', 'mana',
              'stamina', 'backpack', 'money', 'current_hp', 'current_mana', 'current_stamina']
    list_filter = ['hero_class']
    search_fields = ['name']


admin.site.register(Item)

