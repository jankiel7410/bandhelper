from rest_framework import serializers

from boards.models import Song


class SongSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    poster = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'link', 'poster', 'description', 'score', ]

    def save(self, **kwargs):
        kwargs['poster_id'] = self.context['user'].id
        return super().save(**kwargs)
