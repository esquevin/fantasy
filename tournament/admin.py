from django.contrib import admin
from .models import (
    Tournament,
    League,
)

admin.site.register(Tournament)
admin.site.register(League)
