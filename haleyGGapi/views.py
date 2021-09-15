from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from haleyGGapi.serializers import PlayerSerializer
from haleyGGapi.models import Player


class PlayerView(GenericAPIView):
    serializer_class = PlayerSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Player.objects.all()

    def get(self, request):
        serializer = self.serializer_class(
            self.get_queryset(), many=True
        )
        return Response(serializer.data)
