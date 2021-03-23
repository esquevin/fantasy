from django.contrib import admin
from .models import (
    Player,
    PlayerCard,
)

admin.site.register(Player)
admin.site.register(PlayerCard)
