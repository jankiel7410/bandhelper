from rest_framework import serializers

from boards.models import Song, Board, List


class SongSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    poster = serializers.PrimaryKeyRelatedField(read_only=True)
    list = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=List.objects.all())

    class Meta:
        model = Song
        fields = ['id', 'link', 'poster', 'description', 'list', 'score', ]

    def save(self, **kwargs):
        kwargs['poster_id'] = self.context['user'].id
        return super().save(**kwargs)

    def validate_list(self, value):
        if self.instance:  # this is create, not update.
            if not value:
                raise serializers.ValidationError('You must move card somewhere')
            return value
        return List.objects.get(board__admin_id=self.context['user'].id, position=0)


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ['id', 'name', 'position']


class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, source='get_lists', read_only=True)

    class Meta:
        model = Board
        fields = ['admin', 'name', 'lists', ]
