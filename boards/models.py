from functools import lru_cache

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

    @property
    @lru_cache(maxsize=128)
    def score(self):
        res = self.votes.aggregate(models.Avg('score'))
        return res['score__avg'] or 0

    def __str__(self):
        return 'Song #{}: {}'.format(self.id, self.link)
