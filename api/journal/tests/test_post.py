# Testing imports
import pytest
from django.utils.crypto import get_random_string

# Local app imports
from api.models import JournalEntry
from api.journal import post


@pytest.mark.django_db
class TestJournalPostAPI():
    uid='123'
    public_head='hello world!'
    public_body='did it work?'
    private_head='hello again!'
    private_body='secret blog.'
    header_90_chars=get_random_string(length=90)
    header_91_chars=get_random_string(length=91)

    def test_post_public_entry_no_image(self):
        response = post.entry(
            user=self.uid,
            head=self.public_head,
            body=self.public_body,
            image=None,
            public=True
        )
        testEntry = JournalEntry.objects.filter(
            uid=self.uid
        ).latest(
            'id'
        )
        assert response['post'] == 'success!'
        assert testEntry.uid == self.uid
        assert testEntry.head == self.public_head
        assert testEntry.body == self.public_body
        assert not testEntry.image
        assert testEntry.public

    def test_post_private_entry_no_image(self):
        response = post.entry(
            user=self.uid,
            head=self.private_head,
            body=self.private_body,
            image=None,
            public=False
        )
        testEntry = JournalEntry.objects.filter(
            uid=self.uid
        ).latest(
            'id'
        )
        assert response['post'] == 'success!'
        assert testEntry.uid == self.uid
        assert testEntry.head == self.private_head
        assert testEntry.body == self.private_body
        assert not testEntry.image
        assert not testEntry.public

    def test_no_blank_head(self):
        response = post.entry(
            user=self.uid,
            head='',
            body=self.public_body,
            image=None,
            public=True
        )
        assert response['error'] == 'invalid entry head'

    def test_no_blank_body(self):
        response = post.entry(
            user=self.uid,
            head=self.public_head,
            body='',
            image=None,
            public=True
        )
        assert response['error'] == 'invalid entry body'

    def test_no_blank_user(self):
        response = post.entry(
            user='',
            head=self.public_head,
            body=self.public_body,
            image=None,
            public=True
        )
        assert response['error'] == 'invalid user id'

    def test_head_maxlength(self):
        response = post.entry(
            user=self.uid,
            head=self.header_90_chars,
            body=self.public_body,
            image=None,
            public=True
        )
        assert 'error' not in response
        response = post.entry(
            user=self.uid,
            head=self.header_91_chars,
            body=self.public_body,
            image=None,
            public=True
        )
        assert response['error'] == 'invalid entry head'
