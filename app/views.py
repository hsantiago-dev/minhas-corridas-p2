from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.shortcuts import render, redirect
from app.models import User, Race, Interaction
from app.form_race import FormRace


def index(request):
    data = {}

    if request.user.is_authenticated:
        interactions = Interaction.objects.filter(user=request.user)
        print(interactions)
        data['races'] = Race.objects\
            .exclude(id__in=Subquery(interactions.values('race_id'))) \
            .exclude(creator_user=request.user)
    else:
        data['races'] = Race.objects.all()

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
    data['races'] = Race.objects.filter(id=Subquery(interactions.values('race_id')))

    return render(request, 'interested_races.html', data)


@login_required
def registered_races(request):
    data = {}
    interactions = Interaction.objects.filter(user=request.user, interaction='REGISTERED')
    data['races'] = Race.objects.filter(id=Subquery(interactions.values('race_id')))

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
        return redirect('index')

    # return redirect('registration_race')
    return render(request, 'registration_race.html', {'form': form})


@login_required
def edit_race(request, id_race):
    # TODO - Implementar a edição de uma corrida
    data = {}
    data['race'] = Race.objects.get(pk=id_race)
    data['form'] = FormRace(instance=data['race'])

    return render(request, 'registration_race.html', data)


@login_required
def mark_interest(request, id_race):
    # TODO - Implementar a exclusão da interação caso houver
    interaction = Interaction(user=request.user, race=Race.objects.get(pk=id_race), interaction='INTERESTED')
    interaction.save()

    return redirect('index')


@login_required
def subscription(request, id_race):
    # TODO - Implementar a exclusão da interação caso houver
    interaction = Interaction(user=request.user, race=Race.objects.get(pk=id_race), interaction='REGISTERED')
    interaction.save()

    return redirect('index')
