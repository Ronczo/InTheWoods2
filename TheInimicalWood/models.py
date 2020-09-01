from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class Character(models.Model):
    hero_classes = [
        (0, "Knight"),
        (1, "Archer"),
        (2, "Sorcerer"),
    ]

    hero_class = models.PositiveSmallIntegerField(choices=hero_classes, blank=False, null=False, default=0)
    name = models.CharField(max_length=20, unique=True, blank=False)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attack_dmg = models.PositiveSmallIntegerField(blank=False, null=False, default=10)
    defence = models.PositiveSmallIntegerField(blank=False, null=False, default=10)
    hp = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    mana = models.PositiveSmallIntegerField(blank=False, null=False, default=50)
    stamina = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    backpack = JSONField()
    money = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    inventory = JSONField()
    current_hp = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    current_mana = models.PositiveSmallIntegerField(blank=False, null=False, default=50)
    current_stamina = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    mission = models.PositiveSmallIntegerField(blank=False, null=False, default=0)  # Last finished mission
    critical_chance = models.PositiveSmallIntegerField(blank=False, null=False, default=20)

    def __str__(self):
        return f"""NAME: {self.name}
         - attributes:
         -attack damage: {self.attack_dmg}
         -defence: {self.defence}
         -hp: {self.hp}
         -mana: {self.mana}
         -stamina: {self.stamina}
         """


class Item(models.Model):
    item_categories = [
        (0, 'Body'),
        (1, 'Sword'),
        (2, 'Bow'),
        (3, 'Wand'),
        (4, 'Leather'),
        (5, 'Plate'),
        (6, 'Helmet'),
        (7, 'Consumables')
    ]

    name = models.CharField(max_length=20, unique=False, blank=False)
    category = models.PositiveSmallIntegerField(default=0, choices=item_categories, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    bonus_attack_dmg = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_defence = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_hp = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_mana = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_stamina = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    picture = models.URLField(unique=False, blank=True, null=True)
    bonus_current_hp = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_current_mana = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_current_stamina = models.PositiveSmallIntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f"{self.name} - {Item.item_categories[self.category][1].upper()}" \
               f"   (Price: {str(self.price)}, AD: {str(self.bonus_attack_dmg)}, DEF: {str(self.bonus_defence)}" \
               f"HP: {str(self.bonus_hp)}, MANA: {str(self.bonus_mana)}, STAMINA: {str(self.bonus_stamina)}"


class Mission(models.Model):
    number = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    picture = models.URLField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    story = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.number} - {self.description}"


class Monsters(models.Model):
    name = models.CharField(max_length=20, unique=False, blank=False)
    description = models.TextField(blank=True, null=True)
    current_hp = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    current_mana = models.PositiveSmallIntegerField(blank=False, null=False, default=50)
    max_hp = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    max_mana = models.PositiveSmallIntegerField(blank=False, null=False, default=50)
    picture = models.URLField(unique=True, blank=True, null=True)
    number = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    attack_dmg = models.PositiveSmallIntegerField(blank=False, null=False, default=10)
    defence = models.PositiveSmallIntegerField(blank=False, null=False, default=10)
    critical_chance = models.PositiveSmallIntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f"{self.name} - {self.description}"
