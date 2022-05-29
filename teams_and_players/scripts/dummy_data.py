from webbrowser import get
from teams_and_players.models import Team,Player
from predicts.models import Match
import datetime



def create_teams():

    t = Team(
            id = 1,
            name = 'Arsenal',
            country = 'England',
            founded = 1910,
            logo ='https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg'
        )
    t.save()
    print(t.name)

    t = Team(
            id = 2,
            name = 'Liverpool',
            country = 'England',
            founded = 1911,
            logo ='https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/1200px-Liverpool_FC.svg.png'
        )
    t.save()
    print(t.name)


def create_players():
    p = Player(

        player_id = 1,
        name = 'Lacazet',
        age = 29,
        number = 11,
        position = 'F',
        photo = 'models.CharField(max_length=250)',
        team = Team.objects.get(name='Arsenal'),
        )
    p.save()
    print(f"player {p.name} created")

    p = Player(

        player_id = 2,
        name = 'Mane',
        age = 29,
        number = 10,
        position = 'F',
        photo = 'models.CharField(max_length=250)',
        team = Team.objects.get(name='Liverpool'),
        )
    p.save()
    print(f"player {p.name} created")

def create_match():
    current_date = datetime.datetime.now()
    m=Match(
    matchday = 'Matchday 1',
    hTeam = Team.objects.get(name='Arsenal'),
    aTeam = Team.objects.get(name='Liverpool'),
    date = current_date + datetime.timedelta(days=-2),
    status = 'FT',
    hTeamScore = 2,
    aTeamScore = 1,
    #goalScorers = set(Player.objects.filter(name='Mane')),
    match_id = 1,
    league = 'Premier League'
    )
    m.save()
    print(f'match {m.hTeam.name}:{m.aTeam.name} created.')

    m=Match(
    matchday = 'Matchday 1',
    hTeam = Team.objects.get(name='Liverpool'),
    aTeam = Team.objects.get(name='Arsenal'),
    date = current_date + datetime.timedelta(days=5),
    status = 'NS',
    match_id = 2,
    league = 'Premier League'
    )
    m.save()
    print(f'match {m.hTeam.name}:{m.aTeam.name} created.')


    m=Match(
    matchday = 'Matchday 1',
    hTeam = Team.objects.get(name='Arsenal'),
    aTeam = Team.objects.get(name='Liverpool'),
    date = current_date + datetime.timedelta(days=-2),
    status = 'FT',
    hTeamScore = 2,
    aTeamScore = 1,
    #goalScorers = set(Player.objects.filter(name='Mane')),
    match_id = 1,
    league = 'UCL'
    )
    m.save()
    print(f'match {m.hTeam.name}:{m.aTeam.name} created.')

    m=Match(
    matchday = 'Matchday 1',
    hTeam = Team.objects.get(name='Liverpool'),
    aTeam = Team.objects.get(name='Arsenal'),
    date = current_date + datetime.timedelta(days=5),
    status = 'NS',
    match_id = 2,
    league = 'UCL'
    )
    m.save()
    print(f'match {m.hTeam.name}:{m.aTeam.name} created.')

create_match()