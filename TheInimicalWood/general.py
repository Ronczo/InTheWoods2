from django.shortcuts import get_object_or_404
from .models import Item
import smtplib
import json


def create_character_logic(hero):
    """
    Creating character in database used in views.py
    """

    # Creating inventory and backpack
    items = Item.objects.all()
    inventory = {
        'head': 'Head',
        'body': 'Body',
        'left': 'Left',
        'right': 'Right'
    }
    hero.inventory = json.dumps(inventory)

    backpack = {}
    for item in items:
        backpack[item.name] = 0

        # Starting items for every class
        if hero.hero_class == 0:
            backpack["Wooden Sword"] = 1
        elif hero.hero_class == 1:
            backpack["Arrows"] = 50
            backpack["Wooden Bow"] = 1
        elif hero.hero_class == 2:
            backpack["Wooden Wand"] = 1

        backpack["Leather armor"] = 1
        backpack["HP Potion"] = 2
        backpack["Mana Potion"] = 2
    hero.backpack = json.dumps(backpack)

    # starting statistics for everyclass
    if hero.hero_class == 0:
        hero.special_attack_pic = 'http://www.ronczo.webd.pro/media/warrior_special.jpg'
        hero.avatar = 'http://www.ronczo.webd.pro/media/Knight_avatar.jpg'
    elif hero.hero_class == 1:
        hero.avatar = 'http://www.ronczo.webd.pro/media/Archer_avatar.jpg'
        hero.special_attack_pic = 'http://www.ronczo.webd.pro/media/archer_special.jpg'
        hero.attack_dmg = 15
        hero.defence = 5
        hero.stamina = 150
        hero.current_stamina = 150
    elif hero.hero_class == 2:
        hero.avatar = 'http://www.ronczo.webd.pro/media/Sorcerer_avatar.jpg'
        hero.special_attack_pic = 'http://www.ronczo.webd.pro/media/mage_special.jpg'
        hero.attack_dmg = 5
        hero.defence = 5
        hero.mana = 100
        hero.current_mana = 100
    hero.save()


def contact_logic(user_name, user_mail, user_subject, mail_body, account):
    """
     Sending e-mail logic used in views.py
    """
    user = 'theinimicalwood@gmail.com'
    password = 'inimical121'
    mail_to = ["jarosinski91@gmail.com"]
    mail_subject = 'Automatic e-mail from /contact/ from {}({}) - Subject: {}'.format(user_name, user_mail,
                                                                                      user_subject)
    message = """From: {}
       Subject: {} 

       {}
       --------------------------------------
       sent by: {}
       e-mail: {}
       account: {}
       """.format(user_mail, mail_subject, mail_body, user_name, user_mail, account)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(user, password)
    server.sendmail(user_mail, mail_to, message.encode('utf-8'))
    server.close()



class Overview:
    """
    Overview logic used in views.py
    """

    @staticmethod
    def equip_item(request, character, hero_backpack, hero_inventory):
        """
        Equip item - moving to the inventory
        """
        item_to_equip = get_object_or_404(Item, name=request.POST.get('equip'))

        skin = ['Head', 'Body', 'Left', 'Right']
        if item_to_equip.category == 1 or item_to_equip.category == 2 or item_to_equip.category == 3:
            part = 'left'
        elif item_to_equip.category == 4 or item_to_equip.category == 5:
            part = 'body'
        elif item_to_equip.category == 6:
            part = 'head'
        else:
            part = 'right'

        item_to_unequip = get_object_or_404(Item, name=hero_inventory[part])

        # changing quantities in backpack and inventory
        if hero_backpack[item_to_equip.name] > 0 and hero_inventory[part] != item_to_equip.name:

            hero_backpack[item_to_equip.name] -= 1
            if hero_inventory[part] not in skin:
                hero_backpack[hero_inventory[part]] += 1
            character.backpack = json.dumps(hero_backpack)
            if item_to_equip.category != 7:
                hero_inventory[part] = item_to_equip.name
            character.inventory = json.dumps(hero_inventory)

            # unequping item
            character.attack_dmg -= item_to_unequip.bonus_attack_dmg
            character.defence -= item_to_unequip.bonus_defence
            character.hp -= item_to_unequip.bonus_hp
            character.mana -= item_to_unequip.bonus_mana
            character.stamina -= item_to_unequip.bonus_stamina

            # changing stats
            character.attack_dmg += item_to_equip.bonus_attack_dmg
            character.defence += item_to_equip.bonus_defence
            character.hp += item_to_equip.bonus_hp
            character.mana += item_to_equip.bonus_mana
            character.stamina += item_to_equip.bonus_stamina

            # potions
            character.current_hp += item_to_equip.bonus_current_hp
            if character.current_hp > character.hp:
                character.current_hp = character.hp

            character.current_mana += item_to_equip.bonus_current_mana
            if character.current_mana > character.mana:
                character.current_mana = character.mana

            character.current_stamina += item_to_equip.bonus_current_stamina
            if character.current_stamina > character.stamina:
                character.current_stamina = character.stamina

            character.save()

            if item_to_equip.bonus_current_hp > 0:
                message = f"You restores {item_to_equip.bonus_current_hp} HP"
            elif item_to_equip.bonus_current_mana > 0:
                message = f"You restores {item_to_equip.bonus_current_mana} mana"
            elif item_to_equip.bonus_current_stamina > 0:
                message = f"You restores {item_to_equip.bonus_current_stamina} stamina"
            else:
                message = ""


            return message

    @staticmethod
    def take_off_item(request, character, hero_backpack, hero_inventory):
        """
        taking item from inventory to backpack
        """

        item_to_take_off = get_object_or_404(Item, name=request.POST.get('takeoff'))

        if item_to_take_off.category == 1 or item_to_take_off.category == 2 or item_to_take_off.category == 3:
            part = 'left'
            item = 'Left'
        elif item_to_take_off.category == 4 or item_to_take_off.category == 5:
            part = 'body'
            item = "Body"
        elif item_to_take_off.category == 6:
            part = 'head'
            item = 'Head'
        else:
            part = 'right'
            item = 'Right'
        hero_inventory[part] = item
        character.inventory = json.dumps(hero_inventory)

        # changing stats
        character.attack_dmg -= item_to_take_off.bonus_attack_dmg
        character.defence -= item_to_take_off.bonus_defence
        character.hp -= item_to_take_off.bonus_hp
        character.mana -= item_to_take_off.bonus_mana
        character.stamina -= item_to_take_off.bonus_stamina
        if character.current_hp > character.hp:
            character.current_hp = character.hp
        if character.current_mana > character.mana:
            character.current_mana = character.mana
        if character.current_stamina > character.stamina:
            character.current_stamina = character.stamina

        hero_backpack[item_to_take_off.name] += 1
        character.backpack = json.dumps(hero_backpack)

        character.save()

class Shop:
    """
    Actions available in shop
    """

    @staticmethod
    def sell(request, character, hero_backpack):
        """
        selling item
        """
        item_to_sell = get_object_or_404(Item, name=request.POST.get('sell'))
        if hero_backpack[item_to_sell.name] > 0:
            hero_backpack[item_to_sell.name] -= 1
            character.backpack = json.dumps(hero_backpack)
            character.money += item_to_sell.price
            character.save()

    @staticmethod
    def buy(request, character, hero_backpack):
        """
        buying item
        """
        item_to_buy = get_object_or_404(Item, name=request.POST.get('buy'))
        if character.money >= item_to_buy.price:
            character.money -= item_to_buy.price * 1.5
            hero_backpack[item_to_buy.name] += 1
            character.backpack = json.dumps(hero_backpack)
            character.save()
