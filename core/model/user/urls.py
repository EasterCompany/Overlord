# Overlord library
from core.library import path
from core.model.user import views as User


API = lambda endpoint: f"api/user/{endpoint}"
URLS = [

    #
    # User API Endpoints & Functions
    #

    path(
        API("view"),
        User.list_all,
        name="List All Users"
    ),

    path(
        API("view/<str:uuid>"),
        User.view,
        name="View User By ID"
    ),

    path(
        API("delete/<str:uuid>"),
        User.delete,
        name="Delete User by ID"
    ),

    path(
        API("create/<str:email>/<str:permissions>"),
        User.create,
        name="Create New User"
    ),

    path(
        API("verify/<str:target>/<str:key>"),
        User.verify,
        name="Verify New User by Email"
    ),

    path(
        API("edit"),
        User.edit,
        name="Edit Existing User Data"
    ),

    path(
        API("login/<str:emailURI>"),
        User.login,
        name="Login User by Email"
    )

]
