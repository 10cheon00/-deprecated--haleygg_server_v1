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
        ('protoss', 'Protoss'),
        ('terran', 'Terran'),
        ('zerg', 'Zerg'),
        ('random', "Random")
    ]

    name = models.CharField(max_length=30)
    most_race = models.CharField(max_length=10, choices=RACE_LIST, default='R')
    signup_date = models.DateField(default=timezone.now)
    career = models.TextField(
        max_length=1000, default='He has strength, not shown...', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        Player(user=self, race="protoss").save()
        Player(user=self, race="terran").save()
        Player(user=self, race="zerg").save()


class Player(models.Model):
    RACE_LIST = [
        ('protoss', 'Protoss'),
        ('terran', 'Terran'),
        ('zerg', 'Zerg'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    race = models.CharField(max_length=10, choices=RACE_LIST, default='P')

    def __str__(self):
        return f'{self.user} ({self.race})'


class GameResult(models.Model):
    date = models.DateField(default=timezone.now)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, default='')
    game_type = models.CharField(
        max_length=20,
        choices=[
            ('melee', 'Melee'),
            ('top_and_bottom', 'Top And Bottom')],
        default='melee')

    winners = models.ManyToManyField(Player, related_name='winners')
    losers = models.ManyToManyField(Player, related_name='losers')

    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    class Meta:
        ordering = (
            '-date',
            '-league',
            'description'
        )

    def __str__(self):
        return f'{self.date} | {self.league} - {self.description} '

    @classmethod
    def get_player_game_result(cls, name):

        # find 'Player id' with name, not 'Profile id'
        players_id = Player.objects.select_related('user').filter(
            user__name=name).values('id')

        return cls.objects.select_related(
            'league', 'map'
        ).prefetch_related(
            'winners', 'losers', 'winners__user', 'losers__user'
        ).filter(
            Q(winners__id__in=players_id) | Q(losers__id__in=players_id)
        ).distinct()