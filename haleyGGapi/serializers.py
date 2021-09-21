from rest_framework.serializers import ModelSerializer

from haleyGGapi.models import GameResult, Player


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'most_race', 'career', 'signup_date')


class GameResultSerializer(ModelSerializer):
    class Meta:
        model = GameResult
        fields = (
            'id',
            'league_id',
            'round',
            'title',
            'date',
            'winners',
            'losers',
            'map_id'
        )