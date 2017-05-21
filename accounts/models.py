from django.db import models


class Vote(models.Model):
    user = models.ForeignKey('auth.User', related_name='votes')
    song = models.ForeignKey('boards.Song', related_name='votes')
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'song',)
