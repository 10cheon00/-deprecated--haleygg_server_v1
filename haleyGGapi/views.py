from os import read
from django.db.models.functions.window import Rank
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView

from haleyGGapi.serializers import LeagueSerializer
from haleyGGapi.serializers import MapSerializer
from haleyGGapi.serializers import ProfileSerializer
from haleyGGapi.serializers import GameResultSerializer
from haleyGGapi.serializers import RankSerializer
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
        self.serializer_list = []
        self.serialized_data = {}

        self.player_name = kwargs['name']
        self.opponent_name = self.request.query_params.get('versus')

        self.get_player_profile()
        self.get_rank_data()
        self.find_player_rank_from_rank_data()
        if self.opponent_name:
            self.get_opponent_profile()
            self.find_opponent_rank_from_rank_data()
            self.get_player_game_result_list_related_with_opponent()
        else:
            self.get_player_game_result_list()

        return Response(self.serialized_data)

    def get_player_profile(self):
        player_profile = get_object_or_404(
            Profile, 
            name__iexact=self.player_name
        )
        self.serialized_data['player_profile'] = \
            ProfileSerializer(instance=player_profile).data

    def get_opponent_profile(self):
        opponent_profile = get_object_or_404(
            Profile, 
            name__iexact=self.opponent_name
        )
        self.serialized_data['opponent_profile'] = \
            ProfileSerializer(instance=opponent_profile).data

    def get_rank_data(self):
        self.rank_data = Player.get_rank()

    def find_player_rank_from_rank_data(self):
        player_rank = next(
            player_rank for player_rank in self.rank_data \
                if player_rank['player_name'] == self.player_name
        )
        self.serialized_data['player_rank'] = \
            RankSerializer(
                instance=player_rank,
                read_only=True
            ).data
    
    def find_opponent_rank_from_rank_data(self):
        opponent_rank = next(
            opponent_rank for opponent_rank in self.rank_data \
                if opponent_rank['player_name'] == self.opponent_name
        )
        self.serialized_data['opponent_rank'] = \
            RankSerializer(
                instance=opponent_rank,
                read_only=True
            ).data

    def get_player_game_result_list_related_with_opponent(self):
        game_result_list = \
            GameResult.filter.get_player_data_related_with_opponent(
                self.player_name, self.opponent_name
            )
        self.serialized_data['game_result_list'] = \
            GameResultSerializer(
                instance=game_result_list,
                many=True,
                read_only=True
            ).data

    def get_player_game_result_list(self):
        game_result_list = \
            GameResult.filter.get_player_data(self.player_name)
        
        self.serialized_data['game_result_list'] = \
            GameResultSerializer(
                instance=game_result_list,
                many=True,
                read_only=True
            ).data
