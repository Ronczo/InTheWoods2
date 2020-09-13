from django.shortcuts import get_object_or_404
from random import random
from .models import Character, Monsters


class Attacks:
    """
    Your character's basic attach
    """

    @staticmethod
    def basic_attack(id, selected_mission):
        character = get_object_or_404(Character, pk=id)
        monster = get_object_or_404(Monsters, number=selected_mission)

        dmg_factor = round(random() * 100)
        hit_dmg = character.attack_dmg + dmg_factor / 10 - monster.defence / 2

        if dmg_factor < character.critical_chance:
            hit_dmg * 2

        if hit_dmg >= monster.current_hp:
            monster.current_hp = 0
        else:
            monster.current_hp -= hit_dmg

        monster.save()


class Defends:
    """
    Heals your character
    """

    @staticmethod
    def defend(id):
        character = get_object_or_404(Character, pk=id)
        if character.hp - character.current_hp < 10:
            character.current_hp += character.hp - character.current_hp
        else:
            character.current_hp += 10

        character.save()
