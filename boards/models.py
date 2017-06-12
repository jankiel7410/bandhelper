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

    def __str__(self):
        return '%s\'s board: "%s"' % (self.admin, self.name)


class List(models.Model):
    title = models.CharField(max_length=30)
    board = models.ForeignKey('boards.Board', related_name='lists')
    position = models.PositiveSmallIntegerField()

    def __str__(self):
        return '#{} {}'.format(self.id, self.title)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            current_max = List.objects.filter(board_id=self.board_id).aggregate(models.Max('position'))
            pos = 0 if current_max['position__max'] is None else current_max['position__max'] + 1
            self.position = pos
        super().save(force_insert, force_update, using, update_fields)


class Song(models.Model):
    title = models.CharField(max_length=200)
    link = models.TextField(max_length=2000, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    poster = models.ForeignKey('auth.User', related_name='posted_songs')
    list = models.ForeignKey('boards.List', related_name='songs')
    score = models.FloatField(default=0.0)

    def refresh_score(self):
        res = self.votes.aggregate(models.Avg('score'))
        self.score = res['score__avg'] or 0
        self.save()

    def __str__(self):
        return 'Song #{}: {}'.format(self.id, self.link)

    class Meta:
        ordering = ['-score']


@receiver(post_save, sender=User)
def setup_default_board(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance
    b = Board(admin=user, name='My board')
    b.save()
    lists = (List(title='Propositions', board=b, position=0),
             List(title='To try', board=b, position=1),
             List(title='Accepted', board=b, position=2),
             )
    [l.save() for l in lists]
    BoardMembership.objects.create(user=user, board=Board.objects.order_by('id').first())
