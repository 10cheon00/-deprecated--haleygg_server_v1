from rest_framework import serializers

from haleyGGapi.models import League
from haleyGGapi.models import Map
from haleyGGapi.models import Profile
from haleyGGapi.models import Player
from haleyGGapi.models import GameResult


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'type')


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'name', 'type')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'most_race', 'signup_date', 'career')


class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.name')

    class Meta:
        model = Player
        fields = ('name', 'race', 'win_state')


class GameResultSerializer(serializers.ModelSerializer):
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


class NumberOfGamesAndWinsSerializer(serializers.Serializer):
    melee_game_count = serializers.IntegerField()
    melee_win_count = serializers.IntegerField()
    top_and_bottom_game_count = serializers.IntegerField()
    top_and_bottom_win_count = serializers.IntegerField()


class NumberOfGamesAndWinsByEachRaceSerializer(serializers.Serializer):
    pvp_game_count = serializers.IntegerField()
    pvt_game_count = serializers.IntegerField()
    pvz_game_count = serializers.IntegerField()
    tvp_game_count = serializers.IntegerField()
    tvt_game_count = serializers.IntegerField()
    tvz_game_count = serializers.IntegerField()
    zvp_game_count = serializers.IntegerField()
    zvt_game_count = serializers.IntegerField()
    zvz_game_count = serializers.IntegerField()
    
    pvp_win_count = serializers.IntegerField()
    pvt_win_count = serializers.IntegerField()
    pvz_win_count = serializers.IntegerField()
    tvp_win_count = serializers.IntegerField()
    tvt_win_count = serializers.IntegerField()
    tvz_win_count = serializers.IntegerField()
    zvp_win_count = serializers.IntegerField()
    zvt_win_count = serializers.IntegerField()
    zvz_win_count = serializers.IntegerField()


class StatisticsSerializer(
    NumberOfGamesAndWinsSerializer,
    NumberOfGamesAndWinsByEachRaceSerializer
):
    player_name = serializers.CharField(max_length=50)


class WinRankingSerializer(serializers.Serializer):
    melee_win_count_rank = serializers.IntegerField()
    top_and_bottom_win_count_rank = serializers.IntegerField()
