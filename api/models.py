from django.db import models
from django.utils import timezone


class JournalEntry(models.Model):

    class Meta:
        ordering = ['-id']

    uid = models.TextField(
        null=False, blank=False, editable=False
    )
    head = models.TextField(
        null=False, blank=False, default='untitled'
    )
    body = models.TextField(
        null=False, blank=False, default='content'
    )
    likes = models.IntegerField(
        null=False, default=0
    )
    laughs = models.IntegerField(
        null=False, default=0
    )
    sads = models.IntegerField(
        null=False, default=0
    )
    shares = models.IntegerField(
        null=False, default=0
    )
    timestamp = models.DateTimeField(
        null=False, default=timezone.now, editable=False
    )
    public = models.BooleanField(
        null=False, default=True
    )
