# Standard library
import json
from uuid import uuid1
# Django library
from django.db import models
# Overlord library
from core.library.time import get_datetime_str


class Post(models.Model):
    """
    Contains information for related Job Post

    [uid] formatted in this layout 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    [datetime] formated YYYY/MM/DD HH:MM datetime stamp
    [title] any required string
    [subtitle] any optional string
    [genre] any optional string
    [location] any optional string

    [link] optional URL
    [custom_values] json string
    [custom_tags] csv string
    """

    # Essential Fields
    uid = models.CharField(
        primary_key=True,
        unique=True,
        null=False,
        blank=False,
        default=uuid1,
        max_length=32,
    )
    datetime = models.DateTimeField(
        null=False,
        blank=False,
        default=get_datetime_str,
    )
    author_uuid = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        default=None
    )

    # Optional Fields
    header = models.TextField(default="")
    subheader = models.TextField(default="")
    category = models.TextField(default="")
    location = models.TextField(default="")
    image = models.JSONField(default=dict)
    link = models.URLField(default="")

    # Content Fields
    body = models.TextField(default="")
    interactions = models.JSONField(default=dict)
    comments = models.JSONField(default=dict)
    public = models.BooleanField(default=False)

    # Additional Fields
    custom_tags = models.TextField(default="")
    custom_values = models.JSONField(default=dict)

    def __str__(self):
        """
        Return the selected posts uid as a string

        :return str: uid
        """
        return str(self.uid)

    def datestamp(self):
        """
        Return the selected posts timestamp as a string

        :return str: datetime of post
        """
        _stamp = str(self.datetime).split(' ')[0].split('-')
        return f"{_stamp[2]}/{_stamp[1]}/{_stamp[0]}".strip()

    def values(self):
        """
        Return the selected posts custom values as a dictionary

        :return dict: post custom values
        """
        if self.custom_values != '' and self.custom_values != '-':
            return json.loads(self.custom_values)
        else:
            return json.loads("{}")

    def tags(self):
        """
        Return the selected posts custom tags as a list

        :return list: post custom tags
        """
        tags = self.custom_tags.split(',')
        for i, tag in enumerate(tags):
            tags[i] = tag.strip().title()
        return ','.join(tags)
