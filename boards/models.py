from functools import lru_cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class BoardMembership(models.Model):
    user = models.ForeignKey('auth.User', related_name='board_memberships')
    board = models.ForeignKey('boards.Board', related_name='board_memberships')


class Board(models.Model):
    admin = models.ForeignKey('auth.User', related_name='boards')
    name = models.CharField(max_length=30)
    moderators = models.ManyToManyField('auth.User', related_name='moderated_boards')
    members = models.ManyToManyField('auth.User', related_name='shared_boards', through=BoardMembership)
    votes_count_threshold = models.PositiveSmallIntegerField(default=1)

    def get_lists(self):
        return self.lists.order_by('position')


class List(models.Model):
    name = models.CharField(max_length=30)
    board = models.ForeignKey('boards.Board', related_name='lists')
    position = models.PositiveSmallIntegerField()

    def __str__(self):
        return '#{} {}'.format(self.id, self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            current_max = List.objects.filter(board_id=self.board_id).aggregate(models.Max('position'))
            pos = 0 if current_max['position__max'] is None else current_max['position__max']
            self.position = pos
        super().save(force_insert, force_update, using, update_fields)


class Song(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    poster = models.ForeignKey('auth.User', related_name='posted_songs')
    list = models.ForeignKey('boards.List', related_name='songs')

    @property
    @lru_cache(maxsize=128)
    def score(self):
        res = self.votes.aggregate(models.Avg('score'))
        return res['score__avg'] or 0

    def __str__(self):
        return 'Song #{}: {}'.format(self.id, self.link)


@receiver(post_save, sender=User)
def setup_default_board(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance
    b = Board(admin=user, name='My board')
    b.save()
    lists = (List(name='Propositions', board=b),
             List(name='To try', board=b),
             List(name='Accepted', board=b),
             )
    [l.save() for l in lists]
