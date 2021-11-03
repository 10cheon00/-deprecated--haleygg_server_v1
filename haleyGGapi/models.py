from django.utils import timezone
from django.db import models
from django.db.models import Q


class League(models.Model):
    LEAGUE_TYPE = [
        ('Proleague', 'Proleague'),
        ('Starleague', 'Starleague'),
        ('Eventleague', 'Eventleague'),
    ]

    name = models.CharField(max_length=30)
    type = models.CharField(
        max_length=30, choices=LEAGUE_TYPE, default='Proleague')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.type} - {self.name}'


class Map(models.Model):
    MAP_TYPE = [
        ('Melee', 'Melee'),
        ('Top-And-Bottom', 'Top and Bottom'),
    ]
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=20, choices=MAP_TYPE, default='Melee')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    RACE_LIST = [
        ('P', 'Protoss'),
        ('T', 'Terran'),
        ('Z', 'Zerg'),
        ('R', 'Random')
    ]

    name = models.CharField(max_length=30)
    most_race = models.CharField(max_length=5, choices=RACE_LIST, default='R')
    signup_date = models.DateField(default=timezone.now)
    career = models.TextField(
        max_length=1000, default='He has strength, not shown...', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        Player(user=self, race="P").save()
        Player(user=self, race="T").save()
        Player(user=self, race="Z").save()


class Player(models.Model):
    RACE_LIST = [
        ('P', 'Protoss'),
        ('T', 'Terran'),
        ('Z', 'Zerg'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    race = models.CharField(max_length=5, choices=RACE_LIST, default="P")

    def __str__(self):
        return f'{self.user} ({self.race})'


class GameResult(models.Model):
    RACE_LIST = [
        ('P', 'Protoss'),
        ('T', 'Terran'),
        ('Z', 'Zerg'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE)
    # TODO : below fields will be changed to a description.
    round = models.CharField(max_length=30)
    title = models.CharField(max_length=50)

    date = models.DateField(default=timezone.now)

    winners = models.ManyToManyField(Player, related_name='winners')
    losers = models.ManyToManyField(Player, related_name='losers')

    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    class Meta:
        ordering = (
            '-date',
            '-league',
            '-round',
            '-title'
        )

    def __str__(self):
        return f'{self.date} | {self.league} - {self.round} - {self.title} '

    @classmethod
    def get_player_game_result(cls, pk):
        return cls.objects.select_related(
            'map', 'league'
        ).prefetch_related(
            'winners', 'losers'
        ).filter(
            Q(winners__id__in=[pk]) | Q(losers__id__in=[pk])
        )
