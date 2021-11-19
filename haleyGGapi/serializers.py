from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer

from haleyGGapi.models import League
from haleyGGapi.models import Map
from haleyGGapi.models import Profile
from haleyGGapi.models import Player
from haleyGGapi.models import GameResult


class LeagueSerializer(ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'type')


class MapSerializer(ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'name', 'type')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'most_race', 'signup_date', 'career')


class PlayerSerializer(ModelSerializer):
    name = serializers.CharField(source='profile.name')

    class Meta:
        model = Player
        fields = ('name', 'race', 'win_state')


class GameResultSerializer(ModelSerializer):
    league = serializers.CharField(source='league.name')
    map = serializers.CharField(source='map.name')
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = GameResult
        fields = (
            'id',
            'date',
            'league',
            'description',
            'game_type',
            'map',
            'remarks',
            'players'
        )


class RankSerializer(Serializer):
    player_name = serializers.CharField(max_length=30)
    game_count_rank = serializers.IntegerField()
    melee_win_count_rank = serializers.IntegerField()
    top_and_bottom_win_count_rank = serializers.IntegerField()
    versus_protoss_win_count_rank = serializers.IntegerField()
    versus_terran_win_count_rank = serializers.IntegerField()
    versus_zerg_win_count_rank = serializers.IntegerField()
