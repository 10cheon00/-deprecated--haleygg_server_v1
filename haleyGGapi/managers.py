from django.db.models import Manager
from django.db.models import Q

class GameResultFilterManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'league', 'map'
        ).prefetch_related(
            'winners', 
            'losers', 
            'winners__profile', 
            'losers__profile'
        )

    def get_player_data(self, name):
        return self.filter(
            Q(winners__profile__name__iexact=name) |
            Q(losers__profile__name__iexact=name)
        ).distinct()

    def get_player_data_related_with_opponent(
        self, player_name, opponent_name):
        return self.filter(
            (
                Q(winners__profile__name__iexact=player_name) &
                Q(losers__profile__name__iexact=opponent_name)
            ) |
            (
                Q(winners__profile__name__iexact=opponent_name) &
                Q(losers__profile__name__iexact=player_name)
            )
        ).distinct()
