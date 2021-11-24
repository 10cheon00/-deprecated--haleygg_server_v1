from django.urls import path
from django.urls import include
from rest_framework import routers

from haleyGGapi.views import LeagueReadOnlyViewSet
from haleyGGapi.views import MapReadOnlyViewSet
from haleyGGapi.views import GameResultListAPIView
from haleyGGapi.views import ProfileReadOnlyViewSet
from haleyGGapi.views import RetrieveStatisticsView


router = routers.DefaultRouter()
router.register('leagues', LeagueReadOnlyViewSet, basename='leagues')
router.register('maps', MapReadOnlyViewSet, basename='maps')
router.register('profiles', ProfileReadOnlyViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('game-results', GameResultListAPIView.as_view()),
    path('statistics', RetrieveStatisticsView.as_view())
]
