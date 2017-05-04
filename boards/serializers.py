from rest_framework import serializers

from boards.models import Song


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ['id', 'link', 'poster', 'description']
