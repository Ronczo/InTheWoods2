from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, CharacterForm
from .models import Character, Item
from django.contrib.auth.decorators import login_required
import smtplib
import json


def home(request):
    """
    home page
    """
    return render(request, 'home.html')


def signup(request):
    """
    user registration
    """
    something_went_wrong = False
    if request.method == "POST":
        form_signup = RegisterForm(request.POST)
        if form_signup.is_valid():
            form_signup.save()
            return redirect('login')
        else:
            something_went_wrong = True
    else:
        form_signup = RegisterForm()

    return render(request, 'registration/signup.html', {'form_signup': form_signup,
                                                        'something_went_wrong': something_went_wrong})


def aboutme(request):
    return render(request, 'aboutme.html')


@login_required
def contact(request):
    """
    senditg e-mail
    """
    something_went_wrong = False

    user = 'theinimicalwood@gmail.com'
    password = 'inimical121'
    mail_to = ["jarosinski91@gmail.com"]

    user_name = request.POST.get('username')
    user_mail = request.POST.get('usermail')
    account = request.user
    user_subject = request.POST.get('usersubject')
    mail_subject = 'Automatic e-mail from /contact/ from {}({}) - Subject: {}'.format(user_name, user_mail,
                                                                                      user_subject)
    mail_body = request.POST.get('usertext')

    message = """From: {}
    Subject: {} 

    {}
    --------------------------------------
    sent by: {}
    e-mail: {}
    account: {}
    """.format(user_mail, mail_subject, mail_body, user_name, user_mail, account)

    if request.method == 'POST':
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(user, password)
            server.sendmail(user_mail, mail_to, message.encode('utf-8'))
            server.close()
        except:
            something_went_wrong = True
    return render(request, 'contact.html', {'something_went_wrong': something_went_wrong})


@login_required
def game(request):
    """
    selecting character
    """
    user_characters = Character.objects.filter(belongs_to=request.user)
    len_user_characters = len(user_characters)

    context = {
        'user_characters': user_characters,
        'len_user_characters': len_user_characters
    }

    return render(request, 'character_select.html', context)


@login_required
def create_character(request):
    new_character_form = CharacterForm(request.POST or None)

    if new_character_form.is_valid():
        hero = new_character_form.save(commit=False)
        hero.belongs_to = request.user

        # I'm not proud of this part of code :/
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

        if hero.hero_class == 0:
            pass
        elif hero.hero_class == 1:
            hero.attack_dmg = 15
            hero.defence = 5
            hero.stamina = 150
        elif hero.hero_class == 2:
            hero.attack_dmg = 5
            hero.defence = 5
            hero.mana = 100
        hero.save()

        for item in items:
            item.belongs_to_hero.add(hero)

        return redirect(game)

    return render(request, 'create_character.html', {'New_character_form': new_character_form})


@login_required
def delete_character(request, id):
    """
    deletes character from database
    """
    character = get_object_or_404(Character, pk=id)

    if request.method == "POST":
        character.delete()
        return redirect(game)

    return render(request, 'confirmation.html', {'character': character})


def specialthanks(request):
    return render(request, 'specialthanks.html')


@login_required
def overview(request, id):
    """
    character overview
    """
    character = get_object_or_404(Character, pk=id)

    # Creating backpack from JSON string
    hero_backpack = json.loads(character.backpack)
    backpack = {}
    for item in hero_backpack:
        if hero_backpack[item] > 0:
            item_to_add = get_object_or_404(Item, name=item)
            backpack[item_to_add] = hero_backpack[item]

    # Creating inventory from JSON string
    hero_inventory = json.loads(character.inventory)
    inventory = {}
    for item in hero_inventory:
        item_to_add_to_inventory = get_object_or_404(Item, name=hero_inventory[item])
        inventory[item] = item_to_add_to_inventory

    # selling item
    if request.method == "POST":  # TODO: Learn AJAX(?)
        if 'sell' in request.POST:
            item_to_sell = get_object_or_404(Item, name=request.POST.get('sell'))
            if hero_backpack[item_to_sell.name] > 0:
                hero_backpack[item_to_sell.name] -= 1
                character.backpack = json.dumps(hero_backpack)
                character.money += item_to_sell.price
                character.save()
                return redirect(overview, id=character.id)

    # Equip item - moving to the inventory
    if request.method == "POST":
        if 'equip' in request.POST:
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

            # changing quantities in backpack and inventory
            if hero_backpack[item_to_equip.name] > 0 and hero_inventory[part] != item_to_equip.name:

                hero_backpack[item_to_equip.name] -= 1
                if hero_inventory[part] not in skin:
                    hero_backpack[hero_inventory[part]] += 1
                character.backpack = json.dumps(hero_backpack)
                if item_to_equip.category != 7:
                    hero_inventory[part] = item_to_equip.name

                # changing stats
                character.inventory = json.dumps(hero_inventory)
                character.attack_dmg += item_to_equip.bonus_attack_dmg
                character.defence += item_to_equip.bonus_defence
                character.hp += item_to_equip.bonus_hp
                character.mana += item_to_equip.bonus_mana
                character.stamina += item_to_equip.bonus_stamina

                # potions
                if character.hp > item_to_equip.bonus_hp + character.current_hp:
                    character.current_hp += item_to_equip.bonus_current_hp
                else:
                    character.current_hp += (character.hp - character.current_hp)
                if character.mana > item_to_equip.bonus_mana + character.current_mana:
                    character.current_mana += item_to_equip.bonus_current_mana
                else:
                    character.current_mana += (character.mana - character.current_mana)
                if character.stamina > item_to_equip.bonus_stamina + character.current_stamina:
                    character.current_stamina += item_to_equip.bonus_current_stamina
                else:
                    character.current_stamina += (character.stamina - character.current_stamina)

                character.save()
                return redirect(overview, id=character.id)

    # taking item from inventory to backpack
    if request.method == "POST":
        if 'takeoff' in request.POST:
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
            return redirect(overview, id=character.id)

    # Variables needed for template
    loop_index_raw = [i for i in range(1000)][1::3]
    progress_bar_hp = int(character.current_hp / character.hp * 100) if (
                                                                                character.current_hp / character.hp * 100) >= 25 else 25
    progress_bar_mana = int(character.current_mana / character.mana * 100) if (
                                                                                      character.current_mana / character.mana * 100) >= 25 else 25
    progress_bar_stamina = int(character.current_stamina / character.stamina * 100) if (
                                                                                               character.current_stamina / character.stamina * 100) >= 25 else 25
    context = {
        'character': character, 'backpack': backpack,
        'loop_index_raw': loop_index_raw, 'inventory': inventory,
        'progress_bar_hp': progress_bar_hp,
        'progress_bar_mana': progress_bar_mana,
        'progress_bar_stamina': progress_bar_stamina
    }

    return render(request, 'overview.html', context)
