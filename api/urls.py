# Overlord-API imports
from api.user.urls import URLS as USER
from api.posts.urls import URLS as POST
from api.jobs.urls import URLS as JOB
from api.mock.urls import URLS as MOCK
from api.admin.urls import URLS as ADMIN

URLS = \
    USER + POST + JOB + MOCK + ADMIN
