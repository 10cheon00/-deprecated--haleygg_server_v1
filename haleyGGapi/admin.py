from django.contrib import admin

from haleyGGapi.models import GameResult 
from haleyGGapi.models import Profile
from haleyGGapi.models import Player
from haleyGGapi.models import Map
from haleyGGapi.models import League


admin.site.register(GameResult)
admin.site.register(Profile)
admin.site.register(Player)
admin.site.register(Map)
admin.site.register(League)