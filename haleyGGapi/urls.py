from django.urls import path
from django.urls import include
from rest_framework import routers

from haleyGGapi.views import GameResultListAPIView
from haleyGGapi.views import LeagueReadOnlyViewSet
from haleyGGapi.views import MapReadOnlyViewSet
from haleyGGapi.views import RetrieveProfileAPIView
from haleyGGapi.views import ListProfileAPIView
from haleyGGapi.views import RetrieveRankingAPIView
from haleyGGapi.views import RetrieveStatisticsAPIView


router = routers.DefaultRouter()
router.register('leagues', LeagueReadOnlyViewSet, basename='leagues')
router.register('maps', MapReadOnlyViewSet, basename='maps')

urlpatterns = [
    path('', include(router.urls)),
    path('profiles', ListProfileAPIView.as_view()),
    path('profiles/ranks', RetrieveRankingAPIView.as_view()),
    path('profiles/<str:name__iexact>', RetrieveProfileAPIView.as_view()),
    path('profiles/<str:name__iexact>/statistics', RetrieveStatisticsAPIView.as_view()),
    path('game-results', GameResultListAPIView.as_view()),
]
