from django.db import models


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