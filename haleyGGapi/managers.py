from django.db.models import Manager
from django.db.models import Q

class GameResultRelationshipManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'league', 'map'
        ).prefetch_related(
            'players', 
            'players__profile'
        )
