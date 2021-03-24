from django.contrib import admin
from .models import (
    Tournament,
    League,
    Team,
    TeamPlayerCard,
    TournamentPlayerCard,
)

admin.site.register(Tournament)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(TeamPlayerCard)
admin.site.register(TournamentPlayerCard)