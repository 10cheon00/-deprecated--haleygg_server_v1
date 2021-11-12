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
    queryset = GameResult.filter.get_queryset()
    serializer_class = GameResultSerializer


"""
Above viewsets are used by managing data. (create, update, delete...)
TODO 
Create authentication to write data on League, Map, GameResults, Player Model.
Before creating authentication, front client that create data should be finished.

To show data, do not use above viewset, use PlayerInformationRetrieveView.
"""


class RetrievePlayerInformationView(APIView):
    def get(self, *args, **kwargs):
        # must be return profile, gameresult, elo.
        # should use serializer. all return values must be serializer.
        self.serialized_data = {}
        self.player_name = kwargs['name']
        self.opponent_name = self.request.query_params.get('versus')

        self.get_profile()
        self.get_information()

        return Response(self.serialized_data)

    def get_profile(self):
        player_profile = get_object_or_404(
            Profile, 
            name__iexact=self.player_name
        )
        profile_serializer = ProfileSerializer(instance=player_profile).data
        self.serialized_data['player_profile'] = profile_serializer

    def get_information(self):
        if self.opponent_name:
            self.game_result_list = \
                GameResult.filter.get_player_data_related_with_opponent(
                    self.player_name, self.opponent_name
                )
        else:
            self.game_result_list = \
                GameResult.filter.get_player_data(self.player_name)
    
        game_result_serializer = GameResultSerializer(
            instance=self.game_result_list,
            many=True,
            read_only=True
        ).data
        self.serialized_data['game_result_list'] = game_result_serializer
