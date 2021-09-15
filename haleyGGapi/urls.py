from django.urls import path

from haleyGGapi.views import PlayerView


urlpatterns = [
    path('player/', PlayerView.as_view())
]