from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.db.models import Window
from django.db.models.expressions import F
from django.db.models.functions import Rank


class GameResultRelationshipManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'league', 'map'
        ).prefetch_related(
            'players',
            'players__profile'
        )


class RecordMixin(object):
    def get_the_annotated_record_queryset(self):
        self.prepare_annotate()

        self.annotate_melee_record()
        self.annotate_top_and_bottom_record()

        return self.result_queryset

    def get_the_annotated_melee_record_queryset(self):
        self.prepare_annotate()

        self.annotate_melee_record()

        return self.result_queryset

    def prepare_annotate(self):
        self.process_select_related_to_queryset()
        self.filter_queryset_with_league_name()
        self.group_by_profile_name()

    def process_select_related_to_queryset(self):
        self.result_queryset = self.get_queryset().select_related(
            'game_result',
            'profile',
            'game_result__league'
        ).order_by()

    def filter_queryset_with_league_name(self):
        if self.league_name:
            self.result_queryset = self.result_queryset.filter(
                game_result__league__name=self.league_name)

    def group_by_profile_name(self):
        self.result_queryset = self.result_queryset.values(
            'profile__name'
        ).order_by()

    def annotate_melee_record(self):
        self.result_queryset = self.result_queryset.annotate(
            melee_game_count=Count(
                'id',
                filter=Q(game_result__game_type='melee')
            ),
            melee_win_count=Count(
                'id',
                filter=Q(game_result__game_type='melee') & Q(win_state=True)
            ),
            melee_lose_count=Count(
                'id',
                filter=Q(game_result__game_type='melee') & Q(win_state=False)
            )
        )

    def annotate_top_and_bottom_record(self):
        self.result_queryset = self.result_queryset.annotate(
            top_and_bottom_game_count=Count(
                'id',
                filter=Q(game_result__game_type='top_and_bottom')
            ),
            top_and_bottom_win_count=Count(
                'id',
                filter=Q(game_result__game_type='top_and_bottom') &
                Q(win_state=True)
            ),
            top_and_bottom_lose_count=Count(
                'id',
                filter=Q(game_result__game_type='top_and_bottom') &
                Q(win_state=False)
            )
        )


class StatisticsManager(models.Manager, RecordMixin):
    def get_player_statistics_queryset(self, league_name=None, player_name=None):
        self.league_name = league_name

        queryset = self.get_the_annotated_record_queryset_by_each_race().values(
            'melee_game_count',
            'melee_win_count',
            'melee_lose_count',
            'top_and_bottom_game_count',
            'top_and_bottom_win_count',
            'top_and_bottom_lose_count',
            'pvp_game_count',
            'pvt_game_count',
            'pvz_game_count',
            'tvp_game_count',
            'tvt_game_count',
            'tvz_game_count',
            'zvp_game_count',
            'zvt_game_count',
            'zvz_game_count',

            'pvp_win_count',
            'pvt_win_count',
            'pvz_win_count',
            'tvp_win_count',
            'tvt_win_count',
            'tvz_win_count',
            'zvp_win_count',
            'zvt_win_count',
            'zvz_win_count',

            player_name=F('profile__name')
        )
        if player_name:
            queryset = queryset.filter(player_name__iexact=player_name)

        return queryset

    def get_player_statistics_queryset_related_with_opponent(
        self, player_name, opponent_name, league_name=None
    ):
        self.league_name = league_name

        queryset = self.get_the_annotated_melee_record_queryset(
        ).filter(
            profile__name=player_name,
            opponent__profile__name=opponent_name
        ).values(
            'melee_game_count',
            'melee_win_count',
            'melee_lose_count',
            player_name=F('profile__name')
        )[0]

        return queryset

    def get_the_annotated_record_queryset_by_each_race(self):
        return self.get_the_annotated_record_queryset().\
            annotate(
                pvp_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='P') & Q(opponent__race='P')),
                pvt_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='P') & Q(opponent__race='T')),
                pvz_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='P') & Q(opponent__race='Z')),
                tvp_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='T') & Q(opponent__race='P')),
                tvt_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='T') & Q(opponent__race='T')),
                tvz_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='T') & Q(opponent__race='Z')),
                zvp_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='Z') & Q(opponent__race='P')),
                zvt_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='Z') & Q(opponent__race='T')),
                zvz_win_count=Count(
                    'id',
                    filter=Q(win_state=True) &
                    Q(race='Z') & Q(opponent__race='Z')),
                pvp_game_count=Count(
                    'id',
                    filter=Q(race='P') & Q(opponent__race='P')),
                pvt_game_count=Count(
                    'id',
                    filter=Q(race='P') & Q(opponent__race='T')),
                pvz_game_count=Count(
                    'id',
                    filter=Q(race='P') & Q(opponent__race='Z')),
                tvp_game_count=Count(
                    'id',
                    filter=Q(race='T') & Q(opponent__race='P')),
                tvt_game_count=Count(
                    'id',
                    filter=Q(race='T') & Q(opponent__race='T')),
                tvz_game_count=Count(
                    'id',
                    filter=Q(race='T') & Q(opponent__race='Z')),
                zvp_game_count=Count(
                    'id',
                    filter=Q(race='Z') & Q(opponent__race='P')),
                zvt_game_count=Count(
                    'id',
                    filter=Q(race='Z') & Q(opponent__race='T')),
                zvz_game_count=Count(
                    'id',
                    filter=Q(race='Z') & Q(opponent__race='Z')),
        )


class RankingManager(models.Manager, RecordMixin):
    def get_ranking_queryset(self, league_name=None):
        self.league_name = league_name

        return self.get_win_ranking_queryset().values(
            'melee_win_count_rank',
            'top_and_bottom_win_count_rank',

            player_name=F('profile__name')
        )

    def get_win_ranking_queryset(self):
        return self.get_the_annotated_record_queryset().annotate(
            melee_win_count_rank=Window(
                expression=Rank(),
                order_by=F('melee_win_count').desc()
            ),
            top_and_bottom_win_count_rank=Window(
                expression=Rank(),
                order_by=F('top_and_bottom_win_count').desc()
            )
        )
