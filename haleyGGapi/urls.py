from django.urls import path
from django.urls import include
from rest_framework import routers

from haleyGGapi.views import LeagueReadOnlyViewSet
from haleyGGapi.views import MapReadOnlyViewSet
from haleyGGapi.views import GameResultListAPIView
from haleyGGapi.views import ProfileReadOnlyViewSet
from haleyGGapi.views import RetrieveRankView


router = routers.DefaultRouter()
router.register('leagues', LeagueReadOnlyViewSet, basename='league')
router.register('maps', MapReadOnlyViewSet, basename='map')
router.register('profiles', ProfileReadOnlyViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('game-results', GameResultListAPIView.as_view()),
    path('rank', RetrieveRankView.as_view())
]
