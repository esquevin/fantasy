from django.test import TestCase
from django.db import IntegrityError
from .models import User
from .models import Team
from .models import League
from .models import Tournament
from card.models import Player, PlayerCard
from django.utils import timezone
from datetime import timedelta


def complete_team(team: Team, user: User):
    for i in range(5):
        player = Player.objects.create(first_name="", last_name="")
        team.add_player_card(PlayerCard.objects.create(user=user, player=player))


class TeamTests(TestCase):
    def test_team_is_incomplete(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)

        self.assertFalse(team.is_complete())
        self.assertEqual(Team.objects.complete().count(), 0)

    def test_team_is_complete(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)
        complete_team(team, user)

        self.assertTrue(team.is_complete())
        self.assertEqual(Team.objects.complete().count(), 1)

    def test_team_max_size(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)

        player = Player.objects.create(first_name="", last_name="")
        team.add_player_card(PlayerCard.objects.create(user=user, player=player))
        team.add_player_card(PlayerCard.objects.create(user=user, player=player))
        team.add_player_card(PlayerCard.objects.create(user=user, player=player))
        team.add_player_card(PlayerCard.objects.create(user=user, player=player))
        team.add_player_card(PlayerCard.objects.create(user=user, player=player))
        with self.assertRaises(IntegrityError):
            team.add_player_card(PlayerCard.objects.create(user=user, player=player))

    def test_team_doesnt_reuse_card(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)
        player = Player.objects.create(first_name="", last_name="")
        player_card = PlayerCard.objects.create(user=user, player=player)

        team.add_player_card(player_card)
        with self.assertRaises(IntegrityError):
            team.add_player_card(player_card)

    def test_user_can_have_multiple_teams_without_leagues(self):
        user = User.objects.create()
        Team.objects.create(user=user)
        Team.objects.create(user=user)

    def test_user_can_only_have_one_team_per_league(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)
        complete_team(team, user)
        now = timezone.now()
        tournament = Tournament.objects.create(start=now, end=now + timedelta(4))
        league = League.objects.create(tournament=tournament)
        team.sumbit_in(league)

        with self.assertRaises(IntegrityError):
            team2 = Team.objects.create(user=user)
            complete_team(team2, user)
            team2.sumbit_in(league)

    def test_user_can_add_a_team_to_another_league(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)
        complete_team(team, user)

        now = timezone.now()
        tournament = Tournament.objects.create(start=now, end=now + timedelta(4))
        league = League.objects.create(tournament=tournament)
        team.sumbit_in(league)

        other_league = League.objects.create(tournament=tournament)
        team2 = Team.objects.create(user=user)
        complete_team(team2, user)
        team2.sumbit_in(other_league)

    def test_only_complete_team_can_be_submitted(self):
        user = User.objects.create()
        team = Team.objects.create(user=user)
        now = timezone.now()
        tournament = Tournament.objects.create(start=now, end=now + timedelta(4))
        league = League.objects.create(tournament=tournament)

        with self.assertRaises(ValueError):
            team.sumbit_in(league)

        self.assertIsNone(team.league)

        for i in range(5):
            player = Player.objects.create(first_name="", last_name="")
            team.add_player_card(PlayerCard.objects.create(user=user, player=player))
        team.sumbit_in(league)

        self.assertEqual(team.league, league)
