# Overlord library
from core.library import path
from core.models.posts import views as posts

API = lambda endpoint: f"api/post/{endpoint}"
URLS = [

    # =============================== #
    # Posts API Endpoints & Functions #
    # =============================== #

    # List All
    path(
        API("list"),
        posts.list_all,
        name="List All Posts"
    ),

    # Get Post
    path(
        API("get/<uid>"),
        posts.get,
        name="Get Post"
    ),

    # Create Post
    path(
        API("create/<header>/<subheader>/<location>/<genre>/<link>/<custom_tags>/<custom_values>"),
        posts.create,
        name="Create Post"
    ),

    # Update Post
    path(
        API("update/<uid>/<header>/<subheader>/<location>/<genre>/<link>/<custom_tags>/<custom_values>"),
        posts.update,
        name="Update Post"
    ),

    # Attach HTML to Post
    path(
        API("attach/<uid>"),
        posts.attach_html,
        name="Attach HTML to Post"
    ),

    # Delete Post
    path(
        API("delete/<uid>"),
        posts.delete,
        name="Delete Post"
    )

]
