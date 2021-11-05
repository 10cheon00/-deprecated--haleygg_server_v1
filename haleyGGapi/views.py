from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView

from haleyGGapi.serializers import LeagueSerializer
from haleyGGapi.serializers import MapSerializer
from haleyGGapi.serializers import ProfileSerializer
from haleyGGapi.serializers import GameResultSerializer
from haleyGGapi.models import League
from haleyGGapi.models import Player
from haleyGGapi.models import Map
from haleyGGapi.models import Profile
from haleyGGapi.models import GameResult


class LeagueReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class MapReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


class ProfileReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class GameResultReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = GameResult.objects.select_related(
        'league', 'map'
    ).prefetch_related(
        'winners__user', 'losers__user', 'winners__user', 'losers__user'
    ).all()
    serializer_class = GameResultSerializer


"""
Above viewsets are used by managing data. (create, update, delete...)
TODO 
Create authentication to write data on League, Map, GameResults, Player Model.
Before creating authentication, front client that create data should be finished.

To show data, do not use above viewset, use PlayerInformationRetrieveView.
"""


class RetrievePlayerInformationView(APIView):
    def get_object(self, player_name):
        serialized_data = {}

        profile = get_object_or_404(Profile, name=player_name)
        game_results = GameResult.get_player_game_result(player_name)

        serialized_data['profile'] = \
            ProfileSerializer(instance=profile, read_only=True).data
        serialized_data['game_results'] = \
            GameResultSerializer(instance=game_results, many=True, read_only=True).data
        # TODO 
        # Should be added Elo field.
        
        return serialized_data

    def get(self, *args, **kwargs):
        # must be return profile, gameresult, elo.
        # should use serializer. all return values must be serializer.
        player_name = kwargs['name']
        serialized_data = self.get_object(player_name)
        return Response(serialized_data)
