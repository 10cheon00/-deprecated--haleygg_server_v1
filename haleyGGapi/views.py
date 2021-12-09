from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from haleyGGapi.serializers import GameResultSerializer
from haleyGGapi.serializers import LeagueSerializer
from haleyGGapi.serializers import MapSerializer
from haleyGGapi.serializers import MeleeRecordSerializer
from haleyGGapi.serializers import ProfileSerializer
from haleyGGapi.serializers import StatisticsSerializer
from haleyGGapi.serializers import WinRankingSerializer
from haleyGGapi.models import GameResult
from haleyGGapi.models import League
from haleyGGapi.models import Map
from haleyGGapi.models import Player
from haleyGGapi.models import Profile


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


class ListProfileAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    paginator = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveRankingAPIView(APIView):
    def get(self, request):
        self.serialized_data = None
        self.league_name = request.query_params.get('league')
        queryset = Player.ranking.get_ranking_queryset(self.league_name)

        return Response(
            WinRankingSerializer(
                instance=queryset,
                many=True,
                read_only=True
            ).data
        )


class RetrieveProfileAPIView(RetrieveAPIView):
    lookup_field = 'name__iexact'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RetrieveStatisticsAPIView(RetrieveProfileAPIView):
    serialized_data = None

    def get(self, request, *args, **kwargs):
        self.player = self.get_object()
        self.parseParams(request)

        if self.opponent_name:
            return self.get_player_statistics_related_with_opponent()

        return self.get_player_statistics()

    def parseParams(self, request):
        self.league_name = request.query_params.get('league')
        self.opponent_name = request.query_params.get('opponent')

    def get_player_statistics_related_with_opponent(self):
        queryset = Player.statistics.\
            get_player_statistics_queryset_related_with_opponent(
                player_name=self.player.name,
                opponent_name=self.opponent_name
            )

        return Response(
            MeleeRecordSerializer(
                instance=queryset,
                read_only=True
            ).data
        )

    def get_player_statistics(self):
        queryset = Player.statistics.get_player_statistics_queryset(
            self.league_name, self.player.name
        )

        return Response(
            StatisticsSerializer(
                instance=queryset,
                many=True,
                read_only=True
            ).data
        )


class GameResultListAPIView(ListAPIView):
    queryset = GameResult.relationship.get_queryset()
    serializer_class = GameResultSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.league_name:
            queryset = queryset.filter(
                league__name__iexact=self.league_name
            )

        if self.game_type:
            queryset = queryset.filter(
                game_type__iexact=self.game_type
            )

        if self.player_name_list:
            for player_name in self.player_name_list.split(','):
                queryset = queryset.filter(
                    players__profile__name__iexact=player_name
                )
        return queryset.all()

    def get(self, request):
        self.parse_params(request)
        return self.list(self, request)

    def parse_params(self, request):
        self.league_name = request.query_params.get('league')
        self.player_name_list = request.query_params.get('players')
        self.game_type = request.query_params.get('game-type')
