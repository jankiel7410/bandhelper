from rest_framework import serializers

from boards.models import Song, Board, List, BoardMembership


class SongSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    poster = serializers.PrimaryKeyRelatedField(read_only=True)
    board = serializers.PrimaryKeyRelatedField(allow_null=True, write_only=True, queryset=Board.objects.all())  # only when creating Song
    list = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=List.objects.all(), required=False)  # only Admin can use this field

    class Meta:
        model = Song
        fields = ['id', 'link', 'poster', 'description', 'list', 'score', 'board', 'title']

    def validate_board(self, value):
        if not value and not self.instance:  # this is create, but value is not sent
            raise serializers.ValidationError('Board is required on create.')
        elif value and self.instance:
            raise serializers.ValidationError('Song can\'t be moved to other board.')
        return value

    def validate_list(self, value):
        if not self.instance:  # this is create, not update.
            return value

        if not value:
            raise serializers.ValidationError('You must move card somewhere')
        if self.instance.list.board_id != value.board_id:
            raise serializers.ValidationError('You can\'t move cards between boards')
        if self.instance.list_id != value.id and value.board.admin_id != self.context['user'].id:
            raise serializers.ValidationError('Only admin can move card between lanes.')
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
            del attrs['board']
        return attrs


class ListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    cards = SongSerializer(many=True, source='songs')

    class Meta:
        model = List
        fields = ['id', 'title', 'position', 'cards']


class BoardSerializer(serializers.ModelSerializer):
    lanes = ListSerializer(many=True, source='get_lists', read_only=True)

    class Meta:
        model = Board
        fields = ['admin', 'name', 'lanes', ]


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardMembership
        fields = ['id', 'user', 'board']

    def validate(self, attrs):
        if attrs['user'].id == self.context['user'].id:
            raise serializers.ValidationError('Only can\'t invite yourself...')
        if self.context['user'].id != attrs['board'].admin_id:
            raise serializers.ValidationError('Only admin of this board can add members.')
        return attrs