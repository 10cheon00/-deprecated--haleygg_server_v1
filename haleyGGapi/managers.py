from django.db import models
from django.db.models import Manager
from django.db.models import Count
from django.db.models import Q
from django.db.models import Window
from django.db.models import Sum
from django.db.models.expressions import Case
from django.db.models.expressions import F
from django.db.models.expressions import When
from django.db.models.functions import Cast
from django.db.models.functions import Rank


class GameResultRelationshipManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'league', 'map'
        ).prefetch_related(
            'players', 
            'players__profile'
        )


class StatisticsManager(Manager):
    def get_queryset(self, league_name):
        queryset = super().get_queryset().select_related(
            'game_result', 
            'profile', 
            'game_result__league'
        )

        if league_name:
            queryset = queryset.filter(game_result__league__name=league_name)

        return queryset

    def get_win_and_games_count_queryset(self, league_name=None):
        return self.get_queryset(league_name).values('profile__name').order_by().annotate(
            melee_game_count=Count(
                'id',
                filter=Q(game_result__game_type='melee')
            ),
            melee_win_count=Sum(
                Cast('win_state', output_field=models.IntegerField()),
                filter=Q(game_result__game_type='melee')
            ),
            top_and_bottom_game_count=Count(
                'id',
                filter=Q(game_result__game_type='top_and_bottom')
            ),
            top_and_bottom_win_count=Sum(
                Cast('win_state',  output_field=models.IntegerField()),
                filter=Q(game_result__game_type='top_and_bottom')
            )
        ).values(
            'melee_game_count',
            'melee_win_count',
            'top_and_bottom_game_count',
            'top_and_bottom_win_count',
            player_name=F('profile__name')
        )

    def get_winning_rate_queryset(self, league_name=None):
        return self.get_win_and_games_count_queryset(league_name).annotate(
            melee_winning_rate=Case(
                When(
                    melee_game_count=0,
                    then=0
                ),
                default=Cast(
                    F('melee_win_count'),
                    output_field=models.FloatField()
                ) / F('melee_game_count') * 100,
                output_field=models.FloatField()
            ),
            top_and_bottom_winning_rate=Case(
                When(
                    top_and_bottom_game_count=0,
                    then=0
                ),
                default=Cast(
                    F('top_and_bottom_win_count'),
                    output_field=models.FloatField()
                ) / F('top_and_bottom_game_count') * 100,
                output_field=models.FloatField()
            )
        ).values(
            'melee_winning_rate',
            'top_and_bottom_winning_rate',
            'player_name'
        )

    def get_win_count_rank_queryset(self, league_name=None):
        return self.get_win_and_games_count_queryset(league_name).annotate(
            melee_win_count_rank=Window(
                expression=Rank(),
                order_by=F('melee_win_count').desc()
            ),
            top_and_bottom_win_count_rank=Window(
                expression=Rank(),
                order_by=F('top_and_bottom_win_count').desc()
            )
        ).values(
            'melee_win_count_rank',
            'top_and_bottom_win_count_rank',
            'player_name'
        )