from django.db import models

# Create your models here.


class Attachment(models.Model):
    song = models.ForeignKey('boards.Song', related_name='attachments')
    name = models.CharField(max_length=50)
    uploader = models.ForeignKey('auth.User')


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey('boards.Song', related_name='comments')
    poster = models.ForeignKey('auth.User')
    content = models.TextField(max_length=500)
