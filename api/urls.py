# Overlord-API imports
from api.user.urls import URLS as USER
from api.posts.urls import URLS as POST
from api.jobs.urls import URLS as JOB
from api.eastercompany.urls import API as eastercompany

URLS = \
    USER + POST + JOB + eastercompany.URLS
