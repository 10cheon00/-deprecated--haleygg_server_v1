from django.urls import path
from django.urls import include
from rest_framework import routers

from haleyGGapi.views import LeagueReadOnlyViewSet
from haleyGGapi.views import MapReadOnlyViewSet
from haleyGGapi.views import GameResultReadOnlyViewSet
from haleyGGapi.views import ProfileReadOnlyViewSet
from haleyGGapi.views import RetrievePlayerInformationView


router = routers.DefaultRouter()
router.register('league', LeagueReadOnlyViewSet, basename='league')
router.register('map', MapReadOnlyViewSet, basename='map')
router.register('game-result', GameResultReadOnlyViewSet, basename='game-result')
router.register('profile', ProfileReadOnlyViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('player-information/<str:name>', RetrievePlayerInformationView.as_view()),
]
