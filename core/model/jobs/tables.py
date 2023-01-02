# Overlord library
from core.library import models


class JobPost(models.Model):
    """
    Contains information for related Job Post

    [uid] 32 hex digits divided into sections separated by 4 dashes totalling 36 characters
        +   formatted in this layout 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    [datetime]
        +   formatted YYYY/MM/DD HH:MM datetime stamp
    [title] Markdown text document
        +   optional field = ""
    [title] any string provided by the user
        +   required field
    [client] any string provided by the user
        +   optional field = ""
    [website] any string provided by the user represented as a URL
        +   optional field = ""
    [location] any string provided by the user
        +   optional field = ""
    [min_salary] an integer provided by the user
        +   optional field = 0
    [max_salary] an integer provided by the user
        +   optional field = 0
    [applications] a long string containing emails for
        users which have currently applied for this post
        +   optional field = ""
    [requirements] a long string containing recommended
        requirements for each user who applies
        +   optional field = ""
    """

    uid = models.CharField(
        primary_key=True,
        unique=True,
        null=False,
        blank=False,
        max_length=32,
    )

    datetime = models.DateTimeField(
        null=False,
        blank=False,
    )

    info = models.TextField(default="")             # HTML document
    title = models.TextField(default="")            # Job Title
    client = models.TextField(default="")           # Company / Employer
    website = models.TextField(default="")          # Website
    location = models.TextField(default="")         # Location / Remote
    min_salary = models.IntegerField(default=0)     # Minimum advertised salary (if 0 > salary is hidden from applicant)
    max_salary = models.IntegerField(default=0)     # Maximum advertised salary
    requirements = models.TextField(default="")     # Recommended Requirements to apply
    applications = models.JSONField(default=dict, null=True, blank=True)   # Users that have applied already

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
