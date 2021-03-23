from django.contrib import admin
from .models import (
    Tournament,
    League,
    Team,
)

admin.site.register(Tournament)
admin.site.register(League)
admin.site.register(Team)
