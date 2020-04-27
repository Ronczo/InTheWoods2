from django.db import models
from django.contrib.auth.models import User


class Hero(models.Model):
    hero_classes = [
        (0, "Knight"),
        (1, "Archer"),
        (2, "Sorcerer"),
    ]

    hero_class = models.PositiveSmallIntegerField(choices=hero_classes, blank=False, null=False, default=0)
    attack_dmg = models.PositiveSmallIntegerField(blank=False, null=False, default=10)
    defence = models.PositiveSmallIntegerField(blank=False, null=False, default=10)
    hp = models.PositiveSmallIntegerField(blank=False, null=False, default=100)
    mana = models.PositiveSmallIntegerField(blank=False, null=False, default=50)
    stamina = models.PositiveSmallIntegerField(blank=False, null=False, default=100)

    def __str__(self):
        return f"""The {Hero.hero_classes[self.hero_class][1].upper()} attributes:
         -attack damage: {self.attack_dmg}
         -deffence: {self.defence}
         -hp: {self.hp}
         -mana: {self.mana}
         -stamina: {self.stamina}
         """


class Character(Hero):
    name = models.CharField(max_length=20, unique=True, blank=False)
    playable = models.BooleanField(default=True)
    super(Hero)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"""{self.name} - The {self.hero_class} - attributes:
         -attack damage: {self.attack_dmg}
         -deffence: {self.defence}
         -hp: {self.hp}
         -mana: {self.mana}
         -stamina: {self.stamina}
         """


class Item(models.Model):
    weapons_categories = [
        (0, 'Others'),
        (1, 'Sword'),
        (2, 'Bow'),
        (3, 'Wand'),
        (4, 'Leather'),
        (5, 'Bow'),
        (6, 'Sorcerer robe'),
        (9, 'Consumables')
    ]

    name = models.CharField(max_length=20, unique=True, blank=False)
    category = models.PositiveSmallIntegerField(default=0, choices=weapons_categories, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    bonus_attack_dmg = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_defence = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_hp = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_mana = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    bonus_stamina = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    items = models.ManyToManyField(Hero, related_name='items')

    def __str__(self):
        return f"{self.name} - {Item.weapons_categories[self.category][1].upper()}" \
               f"   (Price: {str(self.price)}, AD: {str(self.bonus_attack_dmg)}, DEF: {str(self.bonus_defence)}" \
               f"HP: {str(self.bonus_hp)}, MANA: {str(self.bonus_mana)}, STAMINA: {str(self.bonus_stamina)}"
