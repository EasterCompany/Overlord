# Overlord-API imports
from core.urls import URLS as BASE
from api.user.urls import URLS as USER
from api.posts.urls import URLS as POST
from api.jobs.urls import URLS as JOB
from api.eastercompany.urls import URLS as ADMIN

URLS = \
    USER + POST + JOB + ADMIN + BASE
