from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from card.models import PlayerCard

User = get_user_model()


class Tournament(models.Model):
    """
    ​A tournament has several leagues, starts on Friday and finishes on Monday
    """

    # I went with simple start and end fields. This could be also represented with a
    # year and a week number. But by keeping the model generic it can be reused more
    # easily
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"Tournament {self.start} ({self.end})"


class League(models.Model):
    # Gave a name to my leagues
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} – {self.tournament}"


class TeamManager(models.Manager):
    def complete(self):
        return self.annotate(num_players=models.Count("player_cards")).filter(
            num_players=5
        )


class Team(models.Model):
    """
    A team is made of 5 player cards.
    A user can only have one team per league.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, null=True, on_delete=models.CASCADE)
    player_cards = models.ManyToManyField(PlayerCard, through="TeamPlayerCard")
    objects = TeamManager()

    def is_complete(self):
        return self.player_cards.count() == 5

    def add_player_card(self, player_card: PlayerCard):
        if self.player_cards.count() < 5:
            TeamPlayerCard.objects.create(team=self, player_card=player_card)
        else:
            raise IntegrityError("team cannot have more than 5 player cards")

    def is_submitted(self):
        return self.league is not None

    def sumbit_in(self, league: League):
        if self.is_complete():
            self.league = league
            self.save()
        else:
            raise ValueError("team is not complete")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "league"],
                name="a_user_can_have_one_team_per_league",
            ),
        ]


class TeamPlayerCard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "player_card"],
                name="unicity_of_player_card_in_team",
            ),
        ]
