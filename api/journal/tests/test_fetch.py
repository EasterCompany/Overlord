# Testing imports
import pytest

# Local app imports
from api.models import JournalEntry
from api.journal import fetch


@pytest.mark.django_db
class TestJournalFetchApi():
    uid='123'
    public_head='hello world!'
    public_body='did it work?'
    private_head='hello again!'
    private_body='secret blog.'

    def fake_entry_data(self):
        # plain public journal entry
        JournalEntry.objects.create(
            uid=self.uid,
            head=self.public_head,
            body=self.public_body,
        )
        # plain private journal entry
        JournalEntry.objects.create(
            uid=self.uid,
            head=self.private_head,
            body=self.private_body,
            public=False
        )
        # modified user_id for test_fetch_user_entries test case
        JournalEntry.objects.create(
            uid='123456',
            head=self.private_head,
            body=self.private_body
        )

    def test_fetch_public_entry_by_id(self):
        self.fake_entry_data()
        data = fetch.entry(1)
        assert data['uid'] == self.uid
        assert data['head'] == self.public_head
        assert data['body'] == self.public_body
        assert data['public'] == True

    def test_fetch_private_entry_by_id(self):
        self.fake_entry_data()
        data = fetch.entry(2)
        assert data['uid'] == self.uid
        assert data['head'] == self.private_head
        assert data['body'] == self.private_body
        assert data['public'] == False

    def test_fetch_user_entries(self):
        self.fake_entry_data()
        data = fetch.user_entries(self.uid)
        data = data[self.uid]
        # Confirm amount of entries retrieved
        assert len(data) == 2
        # Confirm all entries are from same user
        for entry in data:
            assert entry['uid'] == self.uid != '123456'
        # Check that data is correct
        assert data[0]['head'] == self.private_head
        assert data[0]['body'] == self.private_body
        assert data[0]['public'] == False
        assert data[1]['head'] == self.public_head
        assert data[1]['body'] == self.public_body
        assert data[1]['public'] == True

    @staticmethod
    def test_fetch_nonexistent_entry():
        data = fetch.entry(404) # Non-existent entry id
        assert 'error' in data  # fetch returns error field
        assert data['error'] == 'JournalEntry matching query does not exist.'

    def test_fetch_latest_user_entry(self):
        self.fake_entry_data()
        data = fetch.latest_entry(self.uid)
        assert 'error' not in data
        assert data['id'] == 2
        assert data['head'] == self.private_head
        assert data['body'] == self.private_body
