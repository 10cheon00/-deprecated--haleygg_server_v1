from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from haleyGGapi.serializers import LeagueSerializer
from haleyGGapi.serializers import MapSerializer
from haleyGGapi.serializers import ProfileSerializer
from haleyGGapi.serializers import GameResultSerializer
from haleyGGapi.serializers import StatisticsSerializer
from haleyGGapi.models import League
from haleyGGapi.models import Player
from haleyGGapi.models import Map
from haleyGGapi.models import Profile
from haleyGGapi.models import GameResult


class LeagueReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    lookup_field = 'name'


class MapReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    lookup_field = 'name'


class ProfileReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'name'


class GameResultListAPIView(GenericAPIView):
    queryset = GameResult.relationship.get_queryset()
    serializer_class = GameResultSerializer

    def get_game_result_list(self):
        queryset = self.queryset

        if self.league_name:
            queryset = queryset.filter(
                league__name__iexact=self.league_name
            )

        if self.player_name_list:
            self.player_name_list = self.player_name_list.split(',')
            for player_name in self.player_name_list:
                queryset = queryset.filter(
                    players__profile__name__iexact=player_name
                )
        return queryset.all()

    def get(self, request, *args, **kwargs):
        self.league_name = request.query_params.get('league')
        self.player_name_list = request.query_params.get('players')
        serializer = self.serializer_class(
            instance=self.get_game_result_list(),
            many=True,
            read_only=True
        )
        return Response(serializer.data)


"""
Above viewsets are used by managing data. (create, update, delete...)
TODO 
Create authentication to write data on League, Map, GameResults, Player Model.
Before creating authentication, front client that create data should be finished.

To show data, do not use above viewset, use PlayerInformationRetrieveView.
"""


class RetrieveStatisticsView(APIView):
    def get(self, request):
        self.serialized_data = None
        self.parse_params(request)
        self.serialize()

        return Response(self.serialized_data)

    def parse_params(self, request):
        self.league_name = request.query_params.get('league')
        self.category = request.query_params.get('category')

    def serialize(self):
        queryset = Player.statistics.get_queryset(self.league_name)
        self.serialized_data = StatisticsSerializer(
            instance=queryset,
            many=True,
            read_only=True
        ).data