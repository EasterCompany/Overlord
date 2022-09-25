# Overlord library
from core.library import path
from core.models.jobs import views as jobs


API = lambda endpoint: f"api/job/{endpoint}"
URLS = [

    # ============================== #
    # Jobs API Endpoints & Functions #
    # ============================== #

    # List All
    path(
        API("list"),
        jobs.list_all,
        name="List All Jobs"
    ),

    # Get Job
    path(
        API("get/<str:uid>"),
        jobs.get,
        name="Get Job"
    ),

    # Create Job
    path(
        API("create/<str:title>/<str:client>/<str:location>/<str:min_salary>/<str:max_salary>"),
        jobs.create,
        name="Create Job"
    ),

    # Update Job
    path(
        API("update/<str:uid>/<str:title>/<str:client>/<str:location>/<str:min_salary>/<str:max_salary>"),
        jobs.update,
        name="Update Job"
    ),

    # Attach HTML to Post
    path(
        API("attach/<uid>"),
        jobs.attach_html,
        name="Attach HTML to Post"
    ),

    # Apply to Job
    path(
        API("apply/<uid>/<fname>/<lname>/<email>/<tel>"),
        jobs.attach_application,
        name="User Apply for Job"
    ),

    # Delete Job
    path(
        API("delete/<str:uid>"),
        jobs.delete,
        name="Delete Job"
    )

]
