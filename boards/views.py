from rest_framework import viewsets

from .models import Song
from .serializers import SongSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsPoster


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsPoster, )

    def get_serializer_context(self):
        return {'user': self.request.user}
