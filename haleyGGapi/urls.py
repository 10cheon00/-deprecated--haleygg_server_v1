from django.urls import path

from haleyGGapi.views import PlayerDetailView
from haleyGGapi.views import PlayerGameResultListView

urlpatterns = [
    path('players/<int:pk>', PlayerDetailView.as_view()),
    path('players/<int:pk>/game-results/', PlayerGameResultListView.as_view() ),
]