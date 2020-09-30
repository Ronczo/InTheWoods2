from django.shortcuts import render, redirect, get_object_or_404
from TheInimicalWood.forms import RegisterForm, CharacterForm, Guest_book
from .models import Character, Item, Mission, Monsters, Guests
from django.contrib.auth.decorators import login_required
from django.views import View
from . import general, combat
import json
from django.http import HttpResponse
from datetime import datetime


class Overview(View):
    """
    character overview - basic stats, inventory, backpack
    """

    @staticmethod
    def get(request, id):
        character = get_object_or_404(Character, pk=id)
        hero_backpack = json.loads(character.backpack)
        hero_inventory = json.loads(character.inventory)

        # Creating backpack from JSON string
        backpack = {}
        for item in hero_backpack:
            if hero_backpack[item] > 0:
                item_to_add = get_object_or_404(Item, name=item)
                backpack[item_to_add] = hero_backpack[item]

        # Creating inventory from JSON string
        inventory = {}
        for item in hero_inventory:
            item_to_add_to_inventory = get_object_or_404(Item, name=hero_inventory[item])
            inventory[item] = item_to_add_to_inventory

        # Variables needed for template
        loop_index_raw = [i for i in range(1000)][1::3]
        progress_bar_hp = int(character.current_hp / character.hp * 100)
        progress_bar_mana = int(character.current_mana / character.mana * 100)
        progress_bar_stamina = int(character.current_stamina / character.stamina * 100)

        context = {
            'character': character,
            'backpack': backpack,
            'loop_index_raw': loop_index_raw,
            'inventory': inventory,
            'progress_bar_hp': progress_bar_hp,
            'progress_bar_mana': progress_bar_mana,
            'progress_bar_stamina': progress_bar_stamina
        }

        return render(request, 'overview.html', context)

    @staticmethod
    def post(request, id):
        character = get_object_or_404(Character, pk=id)
        hero_backpack = json.loads(character.backpack)
        hero_inventory = json.loads(character.inventory)

        if 'equip' in request.POST:
            general.Overview.equip_item(request, character, hero_backpack, hero_inventory)
            return redirect('overview', id=character.id)

        if 'takeoff' in request.POST:
            general.Overview.take_off_item(request, character, hero_backpack, hero_inventory)
            return redirect('overview', id=character.id)


class Shop(View):
    """
    Shop view - buying and selling items
    """

    @staticmethod
    def get(request, id):
        character = get_object_or_404(Character, pk=id)

        # Creating backpack from JSON string
        hero_backpack = json.loads(character.backpack)
        backpack = {}
        for item in hero_backpack:
            if hero_backpack[item] > 0:
                item_to_add = get_object_or_404(Item, name=item)
                backpack[item_to_add] = hero_backpack[item]

        # Preparing shop
        all_items = Item.objects.all()
        items_to_buy = []
        weapons = []
        armors = []
        helmets = []
        consumable = []

        for item in all_items:
            item.price = round(item.price * 1.5)
            if item.category == 1 or item.category == 2 or item.category == 3:
                weapons.append(item)
            elif item.category == 4 or item.category == 5:
                armors.append(item)
            elif item.category == 6:
                helmets.append(item)
            elif item.category == 7:
                consumable.append(item)
            else:
                continue

        context = {
            'character': character,
            'items_to_buy': items_to_buy,
            'backpack': backpack,
            'weapons': weapons,
            'armors': armors,
            'helmets': helmets,
            'consumable': consumable,
        }

        return render(request, 'shop.html', context)

    @staticmethod
    def post(request, id):
        character = get_object_or_404(Character, pk=id)
        hero_backpack = json.loads(character.backpack)

        if 'sell' in request.POST:
            general.Shop.sell(request, character, hero_backpack)
            return redirect('shop', id=character.id)

        if 'buy' in request.POST:
            general.Shop.buy(request, character, hero_backpack)
            return redirect('shop', id=character.id)

        return render(request, 'shop.html')


class Combat(View):
    """
    Fighting mechanics, info about character and monster
    """

    @staticmethod
    def get(request, id, selected_mission):

        character = get_object_or_404(Character, pk=id)
        current_mission = get_object_or_404(Mission, number=selected_mission)
        monster = get_object_or_404(Monsters, number=selected_mission)

        # Variables needed for template
        progress_bar_hp = int(character.current_hp / character.hp * 100)
        progress_bar_mana = int(character.current_mana / character.mana * 100)
        progress_bar_stamina = int(character.current_stamina / character.stamina * 100)

        # Variables for info about monster
        monster_progress_bar_hp = int(monster.current_hp / monster.max_hp * 100)

        battle_course = request.session['battle_route']
        monster_message = request.session['monster_message']
        request.session['battle_route'] = f'The battle is going to start soon. {character.name} is preparing weapon.'
        request.session['monster_message'] = None

        hero_backpack = json.loads(character.backpack)

        # Creating backpack from JSON string
        backpack = {}
        for item in hero_backpack:
            if hero_backpack[item] > 0:
                item_to_add = get_object_or_404(Item, name=item)
                backpack[item_to_add] = hero_backpack[item]

        context = {
            'character': character,
            'current_mission': current_mission,
            'progress_bar_hp': progress_bar_hp,
            'progress_bar_mana': progress_bar_mana,
            'progress_bar_stamina': progress_bar_stamina,
            'mission_number': selected_mission,
            'monster': monster,
            'monster_progress_bar_hp': monster_progress_bar_hp,
            'battle_course': battle_course,
            'monster_message': monster_message,
            'backpack': backpack
        }

        return render(request, 'missions/mission.html', context)

    @staticmethod
    def post(request, id, selected_mission):
        character = get_object_or_404(Character, pk=id)
        current_mission = get_object_or_404(Mission, number=selected_mission)
        hero_backpack = json.loads(character.backpack)
        hero_inventory = json.loads(character.inventory)

        # Player's moves
        if 'attack' in request.POST:
            request.session['battle_route'] = combat.Attacks.basic_attack(id, selected_mission, special=1)
            request.session['monster_message'] = combat.monster_attack(id, selected_mission)
            return redirect('mission', id=character.id, selected_mission=selected_mission)

        if 'defend' in request.POST:
            request.session['battle_route'] = combat.Defends.defend(id)
            request.session['monster_message'] = combat.monster_attack(id, selected_mission)
            return redirect('mission', id=character.id, selected_mission=selected_mission)

        if 'special' in request.POST:
            request.session['battle_route'] = combat.Attacks.basic_attack(id, selected_mission, special=3)
            request.session['monster_message'] = combat.monster_attack(id, selected_mission)
            return redirect('mission', id=character.id, selected_mission=selected_mission)

        if 'won' in request.POST:
            combat.fight_end(id, selected_mission)
            character.mission = current_mission.number
            character.money += current_mission.gold
            character.save()
            return redirect('mission_select', id=character.id)

        if 'lost' in request.POST:
            combat.fight_end(id, selected_mission)
            return redirect('mission_select', id=character.id)

        if 'equip' in request.POST:
            request.session['battle_route'] = general.Overview.equip_item(request, character, hero_backpack,
                                                                          hero_inventory)
            return redirect('mission', id=character.id, selected_mission=selected_mission)


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

    context = {
        'form_signup': form_signup,
        'something_went_wrong': something_went_wrong}

    return render(request, 'registration/signup.html', context)


def aboutme(request):
    """
    about me page
    """
    return render(request, 'aboutme.html')


@login_required
def contact(request):
    """
    sending e-mail to me :)
    """
    something_went_wrong = False
    if request.method == 'POST':
        try:
            general.contact_logic(request.POST.get('username'), request.POST.get('usermail'),
                                  request.POST.get('usersubject'), request.POST.get('usertext'), request.user)
        except Exception:
            something_went_wrong = True

    return render(request, 'contact.html', {'something_went_wrong': something_went_wrong})


@login_required
def game(request):
    """
    selecting character to play
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
    """
    creating new character in database
    """
    new_character_form = CharacterForm(request.POST or None)

    if new_character_form.is_valid():
        hero = new_character_form.save(commit=False)
        hero.belongs_to = request.user
        general.create_character_logic(hero)
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
    """
    Special thanks for help and copyrights
    """
    return render(request, 'specialthanks.html')


@login_required
def mission_select(request, id):
    """
    progress overview and choosing mission
    """
    character = get_object_or_404(Character, pk=id)
    missions = Mission.objects.all()
    next_mission = character.mission + 1

    context = {
        'character': character,
        'missions': missions,
        'next_mission': next_mission
    }

    return render(request, 'mission_select.html', context)


@login_required
def briefing(request, id, selected_mission):
    """
    Showing basic info about selected mission
    """

    character = get_object_or_404(Character, pk=id)
    current_mission = get_object_or_404(Mission, number=selected_mission)

    context = {
        'character': character,
        'current_mission': current_mission,
    }

    return render(request, 'missions/briefing-template.html', context)


@login_required
def guest_book(request):
    try:
        all_registries = Guests.objects.all()
    except:
        all_registries = None

    context = {
        'all_registries': all_registries
    }

    return render(request, 'guest_book.html', context)


@login_required
def guest_book_new(request):
    geust_book_form = Guest_book(request.POST or None)

    if geust_book_form.is_valid():
        registry = geust_book_form.save(commit=False)
        registry.published_date = datetime.now()
        registry.save()
        return redirect(guest_book)

    context = {
        'geust_book_form': geust_book_form
    }

    return render(request, 'guest_book_new.html', context)