from django.db import models
# Create your models here.


class Board(models.Model):
    admin = models.ForeignKey('auth.User', related_name='boards')
    name = models.CharField(max_length=30)
    moderators = models.ManyToManyField('auth.User', related_name='moderated_boards')
    members = models.ManyToManyField('auth.User', related_name='shared_boards')
    votes_count_threshold = models.PositiveSmallIntegerField(default=1)
    proposed_songs = models.ManyToManyField('boards.Song', through='boards.List')


class List(models.Model):
    board = models.ForeignKey('boards.Board')
    song = models.ForeignKey('boards.Song')


class Song(models.Model):
    link = models.URLField()
    poster = models.ForeignKey('auth.User', related_name='posted_songs')
    description = models.TextField(max_length=2000, blank=True, null=True)
