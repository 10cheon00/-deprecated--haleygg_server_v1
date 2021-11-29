from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from haleyGGapi.serializers import LeagueSerializer
from haleyGGapi.serializers import MapSerializer
from haleyGGapi.serializers import ProfileSerializer
from haleyGGapi.serializers import GameResultSerializer
from haleyGGapi.serializers import StatisticsSerializer
from haleyGGapi.serializers import WinRankingSerializer
from haleyGGapi.models import League
from haleyGGapi.models import Player
from haleyGGapi.models import Map
from haleyGGapi.models import Profile
from haleyGGapi.models import GameResult


class LeagueReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    lookup_field = 'name'
    paginator = None


class MapReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    lookup_field = 'name'
    paginator = None


class ProfileReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'name'
    paginator = None


class GameResultListAPIView(ListAPIView):
    queryset = GameResult.relationship.get_queryset()
    serializer_class = GameResultSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.league_name:
            queryset = queryset.filter(
                league__name__iexact=self.league_name
            )

        if self.player_name_list:
            for player_name in self.player_name_list.split(','):
                queryset = queryset.filter(
                    players__profile__name__iexact=player_name
                )
        return queryset.all()

    def get(self, request):
        self.league_name = request.query_params.get('league')
        self.player_name_list = request.query_params.get('players')
        return self.list(self, request)


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
        self.parseParams(request)

        queryset = Player.statistics.get_statistics_queryset(
            self.league_name, 
            self.player_name)

        return Response(
            StatisticsSerializer(
                instance=queryset,
                many=True,
                read_only=True
            ).data)

    def parseParams(self, request):
        self.league_name = request.query_params.get('league')
        self.player_name = request.query_params.get('player')
        

class RetrieveRankingView(APIView):
    def get(self, request):
        self.serialized_data = None
        self.league_name = request.query_params.get('league')
        queryset = Player.ranking.get_ranking_queryset(self.league_name)

        return Response(
            WinRankingSerializer(
                instance=queryset,
                many=True,
                read_only=True
            ).data)