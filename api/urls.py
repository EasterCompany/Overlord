# Overlord-API imports
from api.user.urls import URLS as USER
from api.posts.urls import URLS as POST
from api.jobs.urls import URLS as JOB

URLS = \
    USER + POST + JOB
