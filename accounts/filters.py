import django_filters
from django.contrib.auth.models import User


class UserFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = []
