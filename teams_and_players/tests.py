from django.test import TestCase
from teams_and_players.models import Team

# Create your tests here.


class test_models(TestCase):

    def test_teams(self):

        arsenal = Team(
            id = 1,
            name = 'Arsenal',
            country = 'England',
            founded = 1910,
            logo ='https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg'
        )
        arsenal.save()

        liverpool = Team(
            id = 2,
            name = 'Liverpool',
            country = 'England',
            founded = 1911,
            logo ='https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/1200px-Liverpool_FC.svg.png'
        )
        liverpool.save()