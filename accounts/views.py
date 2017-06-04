from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from accounts import models
from accounts import serializers
from boards.permissions import IsAuthenticatedOrReadOnly, IsPosterOrAdmin


class VoteViewSet(viewsets.ModelViewSet):
    queryset = models.Vote.objects.all()
    serializer_class = serializers.VoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        return {'user': self.request.user}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ['username', ]


class SessionViewSet(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.SessionSerializer
    http_method_names = ['options', 'post']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializers.UserSerializer(instance=request.user).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
