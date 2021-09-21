
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from haleyGGapi.serializers import PlayerSerializer
from haleyGGapi.serializers import GameResultSerializer
from haleyGGapi.models import GameResult, Player


class PlayerDetailView(RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_object(self):
        player = super().get_object()
        return player


class PlayerGameResultListView(APIView):
    def get(self, request, *args, **kwargs):
        results = GameResult.get_player_game_result(kwargs.pop('pk'))
        serializer = GameResultSerializer(results, many=True)
        return Response(serializer.data)
