from rest_framework import serializers

from boards.models import Song, Board, List, BoardMembership


class SongSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    poster = serializers.PrimaryKeyRelatedField(read_only=True)
    board = serializers.PrimaryKeyRelatedField(allow_null=True, write_only=True, queryset=Board.objects.all())  # only when creating Song
    list = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=List.objects.all())  # only Admin can use this field

    class Meta:
        model = Song
        fields = ['id', 'link', 'poster', 'description', 'list', 'score', 'board']

    def validate_board(self, value):
        if not value and not self.instance:  # this is create, but value is not sent
            raise serializers.ValidationError('Board is required on create.')
        elif value and self.instance:
            raise serializers.ValidationError('Song can\'t be moved to other board.')
        return value

    def validate_list(self, value):
        if self.instance:  # this is create, not update.
            if not value:
                raise serializers.ValidationError('You must move card somewhere')
            return value
        return value

    def validate(self, attrs):
        # check is song poster has right to add to that board
        attrs['poster'] = self.context['user']
        poster = attrs['poster']
        if not self.instance:  # it's a create
            board = attrs['board']
            if poster.id != board.admin_id and not board.members.filter(id=poster.id).exists():
                raise serializers.ValidationError('You don\'t have right to add a song to this board.')

            attrs['list'] = List.objects.get(board=board, position=0)


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ['id', 'name', 'position']


class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, source='get_lists', read_only=True)

    class Meta:
        model = Board
        fields = ['admin', 'name', 'lists', ]


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardMembership
        fields = ['id', 'user', 'board']
