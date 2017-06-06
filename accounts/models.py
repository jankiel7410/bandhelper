from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Vote(models.Model):
    user = models.ForeignKey('auth.User', related_name='votes')
    song = models.ForeignKey('boards.Song', related_name='votes')
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'song',)


@receiver([post_save, post_delete], sender=Vote)
def refresh_avg_score(sender, instance, **kwargs):
    instance.song.refresh_score()
