from django.utils import timezone
from django.db import models


class League(models.Model):
    LEAGUE_TYPE = [
        ('Starleague', 'Starleague'),
        ('Proleague', 'Proleague'),
        ('Eventleague', 'Eventleague'),
    ]

    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=LEAGUE_TYPE, default='Starleague')

    class Meta:
        ordering = ['name']


class Player(models.Model):
    RACE_LIST = [
        ('T', 'Terran'),
        ('P', 'Protoss'),
        ('Z', 'Zerg'),
        ('R', 'Random')
    ]

    name = models.CharField(max_length=30)
    most_race = models.CharField(max_length=10, choices=RACE_LIST, default='R')
    signup_date = models.DateField(default=timezone.now)
    career = models.TextField(max_length=1000, default="")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# class Map(models.Model):
#     MAP_TYPE = [
#         ('Melee', 'Melee'),
#         ('Top-And-Bottom', 'Top and Bottom'),
#     ]
#     name = models.CharField(max_length=30)
#     type = models.CharField(max_length=10, choices=MAP_TYPE, default='Melee')

#     class Meta:
#         ordering = ['name']


# class GameResult(models.Model):
#     # 21.03.23	HPL S6 Round17 우수만 vs s-class set 3	haha	t	crazybird	p	네오실피드	crazybird	패	2 연패	-2	6
#     # 21.03.23	HPL S6 Round17 우수만 vs s-class set 3	haha	t	crazybird	p	네오실피드	haha	승	1 연승	1	4

#     league = models.ForeignKey(League, on_delete=models.CASCADE)
#     round = models.CharField(max_length=30)
#     date = models.DateField(default=timezone.now)
#     # player_a = 
#     # player_b = 
#     # winner = 
#     map = models.ForeignKey(Map, on_delete=models.CASCADE)
#     # player_a_race = 
#     # player_b_race = 

#     class Meta:
#         ordering = (
#             '-date',
#             '-league',
#             '-round'
#         )
