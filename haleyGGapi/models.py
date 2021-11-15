from typing import overload
from django.utils import timezone
from django.db import models
from django.db.models import Q

from haleyGGapi.managers import GameResultFilterManager


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
        ('R', "Random")
    ]

    name = models.CharField(max_length=30)
    most_race = models.CharField(max_length=10, choices=RACE_LIST, default='R')
    signup_date = models.DateField(default=timezone.now)
    career = models.TextField(
        max_length=1000, default='He has strength, not shown...', blank=True)

    # TODO
    # 랭킹 정보를 계산하기 위해,
    # 이 곳에 승리 수, 경기 수 등등을 저장해야 한다. 
    # 매 전적 Create, Update, Delete시 이 곳에 있는 데이터를 
    # 수정해야 한다. GameResult 모델에서 담당하면 되겠다.

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)


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
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=20, default="", blank=True)

    objects = models.Manager()
    filter = GameResultFilterManager()

    class Meta:
        ordering = (
            '-date',
            '-league',
            '-id',
            '-description'
        )

    def __str__(self):
        return f'{self.date} | {self.league} - {self.description}'


class Player(models.Model):
    RACE_LIST = [
        ('P', 'Protoss'),
        ('T', 'Terran'),
        ('Z', 'Zerg'),
    ]
    game_result = models.ForeignKey(
        GameResult, 
        on_delete=models.CASCADE,
        related_name="players",
        null=True)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE, 
        null=True,
        related_name="players")
    race = models.CharField(max_length=10, choices=RACE_LIST, default='P')
    win_state = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile} ({self.race}) | {self.game_result}'


class Elo(models.Model):
    date = models.DateField(default=timezone.now)
    
    # TODO
    # elo값과 연결된 profile을 필드로 갖고 있어야?

    class Meta:
        ordering = ('-date',)
