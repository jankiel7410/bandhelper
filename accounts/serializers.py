from django.contrib.auth import authenticate, login
from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import Vote


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password1')

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError('passwords must match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.user = authenticate(**attrs)
        if not self.user:
            raise serializers.ValidationError('You entered incorrect username or password')
        return attrs

    def create(self, validated_data):
        login(self.context['request'], self.user)
        return self.user


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('user', 'song', 'score', )

    def validate_score(self, score: int):
        if score > 5 or score <= 0:
            raise serializers.ValidationError("Score must be between 1 and 5")
        return score

    def save(self, **kwargs):
        self.instance = Vote.objects.filter(song=self.validated_data['song'], user=self.context['user']).first()
        kwargs['user_id'] = self.context['user'].id
        return super().save(**kwargs)
