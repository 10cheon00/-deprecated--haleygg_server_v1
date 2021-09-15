from rest_framework.serializers import ModelSerializer

from haleyGGapi.models import Player
from haleyGGapi.models import League


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id', 'name', 'most_race', 'signup_date', 'career'
        )
