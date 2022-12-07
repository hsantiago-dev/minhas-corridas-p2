from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.shortcuts import render, redirect
from app.models import User, Race, Interaction, RaceCommentary
from app.form_race import FormRace
from app.enums.comment_tag_enum import CommentTag
from enum import Enum
from datetime import datetime, timedelta
from django.utils import timezone


def index(request):
    data = {}

    month_selected = request.GET.get('month')

    if not month_selected:
        month_selected = str(timezone.now().year) + '-' + str(timezone.now().month).zfill(2)

    if request.user.is_authenticated:
        city_selected = request.GET.get('city')
        max_value_selected = request.GET.get('max_value')

        interactions = Interaction.objects.filter(user=request.user)

        if city_selected:

            if not max_value_selected:
                max_value_selected = 1000000
                data['max_value_selected'] = ''
            else:
                data['max_value_selected'] = max_value_selected

            data['city_selected'] = city_selected
            data['races'] = Race.objects \
                .filter(registration_deadline__gte=timezone.now()) \
                .filter(city__contains=city_selected) \
                .filter(registration_value__lte=max_value_selected) \
                .filter(registration_deadline__year=month_selected.split('-')[0]) \
                .filter(registration_deadline__month=month_selected.split('-')[1]) \
                .exclude(id__in=Subquery(interactions.values('race_id'))) \
                .exclude(creator_user=request.user)
        elif max_value_selected:
            data['max_value_selected'] = max_value_selected

            data['races'] = Race.objects \
                .filter(registration_deadline__gte=timezone.now()) \
                .filter(registration_value__lte=max_value_selected) \
                .filter(registration_deadline__year=month_selected.split('-')[0]) \
                .filter(registration_deadline__month=month_selected.split('-')[1]) \
                .exclude(id__in=Subquery(interactions.values('race_id'))) \
                .exclude(creator_user=request.user)
        else:
            data['races'] = Race.objects \
                .filter(registration_deadline__gte=timezone.now()) \
                .filter(registration_deadline__year=month_selected.split('-')[0]) \
                .filter(registration_deadline__month=month_selected.split('-')[1]) \
                .exclude(id__in=Subquery(interactions.values('race_id'))) \
                .exclude(creator_user=request.user)
    else:
        data['races'] = Race.objects \
            .filter(registration_deadline__gte=timezone.now()) \
            .filter(registration_deadline__year=month_selected.split('-')[0]) \
            .filter(registration_deadline__month=month_selected.split('-')[1]) \

    data['month_selected'] = month_selected

    data['cities'] = Race.objects.values_list('city', flat=True).distinct()

    return render(request, 'index.html', data)


def registration_user(request):
    return render(request, 'registration_user.html')


def login(request):
    return render(request, 'login.html')


def insert_user(request):
    if request.POST['name'] and request.POST['email'] and request.POST['password']:
        user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
        user.name = request.POST['name']
        user.save()
        return redirect('login')

    return redirect('registration_user')


@login_required
def interested_races(request):
    data = {}
    interactions = Interaction.objects.filter(user=request.user, interaction='INTERESTED')
    data['races'] = Race.objects\
        .filter(id__in=Subquery(interactions.values('race_id')))\
        .filter(registration_deadline__gte=timezone.now()) \

    return render(request, 'interested_races.html', data)


@login_required
def registered_races(request):
    data = {}
    interactions = Interaction.objects.filter(user=request.user, interaction='REGISTERED')
    data['races'] = Race.objects \
        .filter(id__in=Subquery(interactions.values('race_id'))) \
        .filter(registration_deadline__gte=timezone.now())

    return render(request, 'registered_races.html', data)


@login_required
def races_created(request):
    data = {'races': Race.objects.filter(creator_user_id=request.user.id)}

    return render(request, 'races_created.html', data)


@login_required
def registration_race(request):
    return render(request, 'registration_race.html')


@login_required
def insert_race(request):

    request.POST._mutable = True
    request.POST['creator_user'] = request.user.id

    form = FormRace(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('races_created')

    return render(request, 'registration_race.html', {'form': form})


@login_required
def edit_race(request, id_race):

    data = dict()
    data['race'] = Race.objects.get(pk=id_race)
    data['form'] = FormRace(instance=data['race'])

    return render(request, 'registration_race.html', data)


@login_required
def update_race(request, id_race):

    request.POST._mutable = True
    request.POST['creator_user'] = request.user.id

    data = dict()
    data['race'] = Race.objects.get(pk=id_race)
    form = FormRace(request.POST or None, instance=data['race'])

    if form.is_valid():
        form.save()
        return redirect('races_created')


@login_required
def mark_interest(request, id_race):
    interaction = Interaction.objects.filter(race_id=id_race, user_id=request.user)

    if interaction.exists():
        interaction.update(interaction='INTERESTED')
    else:
        interaction = Interaction(user=request.user, race=Race.objects.get(pk=id_race), interaction='INTERESTED')
        interaction.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def subscription(request, id_race):

    interaction = Interaction.objects.filter(race_id=id_race, user_id=request.user)

    if interaction.exists():
        interaction.update(interaction='REGISTERED', receive_notifications=True)
    else:
        interaction = Interaction(user=request.user, race=Race.objects.get(pk=id_race), interaction='REGISTERED')
        interaction.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def undo_interaction(request, id_race):

    Interaction.objects.filter(race_id=id_race, user_id=request.user).delete()

    return redirect(request.META.get('HTTP_REFERER'))


def commentaries_race(request, id_race):
    data = {
        'race': Race.objects.get(pk=id_race)
        , 'commentaries': RaceCommentary.objects.filter(race_id=id_race).select_related('user')
    }

    return render(request, 'commentaries_race.html', data)


@login_required
def put_commentary(request, id_race):
    commentary = RaceCommentary(user=request.user
                                , race=Race.objects.get(pk=id_race)
                                , commentary=request.POST['commentary']
                                , tag=CommentTag(int(request.POST['tag'])).name
                                , date=datetime.now())

    commentary.save()

    return redirect('/commentaries_race/' + str(id_race))


@login_required
def sticky_notes(request):

    start_date = timezone.now()
    end_date = timezone.now() + timedelta(days=5)

    races_registered = set()

    for i in Interaction.objects.select_related('race').filter(user_id=request.user, interaction='REGISTERED',
                                                               receive_notifications=True):

        if start_date <= i.race.start_date <= end_date:
            races_registered.add(i.race)

    races_interested = set()

    for i in Interaction.objects.select_related('race').filter(user_id=request.user, interaction='INTERESTED',
                                                               receive_notifications=True):

        if start_date <= i.race.registration_deadline <= end_date:
            races_interested.add(i.race)

    data = {
        'races_registered': races_registered,
        'races_interested': races_interested
    }

    return render(request, 'sticky_notes.html', data)


@login_required
def undo_notifications(request, id_race):

    interaction = Interaction.objects.filter(race_id=id_race, user_id=request.user)

    if interaction.exists():
        interaction.update(receive_notifications=False)

    return redirect(request.META.get('HTTP_REFERER'))
