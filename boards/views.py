from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Song, Board
from .serializers import SongSerializer, BoardSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsPoster


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPoster, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ['list']

    def get_serializer_context(self):
        return {'user': self.request.user}


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsPoster, )

    def get_object(self):
        return self.get_queryset().filter(admin_id=self.kwargs['pk']).first()
