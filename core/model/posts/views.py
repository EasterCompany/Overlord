# Standard library
from urllib import parse
# Overlord library
from core.library import api, time, uuid
from core.model.posts.tables import Post


def list_all(req, *args, **kwargs):
    """
    Returns a list of all Title, Client, Location, Salary & Timestamp combinations within the database

    [   ["Title", "Client" ... ] <-- Table Headers
        [[], [],  [], []   ... ] <-- Table Row & Data ]

    formatted for use with a table to be presented like this (below):

    H1          H2          H3
    -------     -------     -------
    ..          ..          ..
    ..          ..          ..
    """
    try:
        # Prepare Output
        def __body__(body_query):
            """
            Contains instructions on how to generate the table content for the front end application

            :param body_query querySet: django query set
            :return json: api table
            """
            body_row_data = []
            for post in body_query:
                body_row_data.append([
                    str(post.uid),
                    str(post.header).title(),
                    str(post.subheader).title(),
                    str(post.location).title(),
                    str(post.category).title(),
                    "✔️" if post.link != "-" else "❌",
                    post.datestamp()
                ])
            return body_row_data
        # Table Response
        return api.table(
            Table=Post,
            Headers=['UID', 'Header', 'Subheader', 'Location', 'Category', 'Link', 'Date'],
            Body=__body__,
            filter={ "order_by": "-datetime" }
        )
    except Exception as exception:
        # Unexpected Error Response
        return api.error(f'[ERROR] when listing Posts:\n\t{exception}')


def get(req, uid, *args, **kwargs):
    """
    Returns a dictionary of Post data

    :param uid str: unique identifier
    :return: api.std
    """
    try:
        # Consume Input
        uid = parse.unquote(uid)
        # Fetch Data
        post = Post.objects.filter(uid=uid).first()
        # Standard Response
        return api.std(
            status=api.OK,
            message={
                'uid': str(post.uid),
                'header': str(post.header).title(),
                'subheader': str(post.subheader).title(),
                'location': str(post.location).title(),
                'category': str(post.category).title(),
                'link': str(post.link),
                'tags': str(post.tags()),
                'values': post.values(),
                'date': post.datestamp(),
                'body': str(post.body)
            }
        )
    except Exception as exception:
        # Unexpected Error Response
        return api.error(f"[ERROR] when fetching a Post:\n\t{exception}")


def create(
    req,
    header, subheader="-", location="-", category="-",
    link="-", custom_tags="-", custom_values="-",
    *args, **kwargs
):
    """
    Create a new Generic Post

    :param header str:
    :param subheader str:
    :param location str:
    :param category str:
    :param link str:
    :param tags str: CSVs as a string
    :param values str: JSON values as a string
    :return json: api.std
    """
    try:
        # Consume Input
        uid = uuid()
        header = parse.unquote(header).lower().strip()
        subheader = parse.unquote(subheader).lower().strip()
        location = parse.unquote(location).lower().strip()
        category = parse.unquote(category).lower().strip()
        link = parse.unquote(link).strip()
        tags = parse.unquote(custom_tags).lower().strip()
        values = parse.unquote(custom_values).lower().strip()
        # Create Post
        Post.objects.create(
            uid=uid,
            datetime=time.get_datetime_string(),
            header=header,
            subheader=subheader,
            location=location,
            category=category,
            link=link,
            custom_tags=tags,
            custom_values=values
        )
        # Standard Response
        return api.std(message=uid, status=api.OK)
    except Exception as exception:
        # Unexpected Error Response
        return api.error(f'[ERROR] when creating a Post:\n\t{exception}')


def update(
    req,
    uid, header, subheader="-", location="-", category="-",
    link="-", custom_tags="-", custom_values="-",
    *args, **kwargs
):
    """
    Updates the specified record belonging to the given `uid` with new data

    :param header str:
    :param subheader str:
    :param location str:
    :param category str:
    :param link str:
    :param tags str: CSVs as a string
    :param values str: JSON values as a string
    :return json: api.std
    """
    try:
        # Consume Input
        _post = Post.objects.filter(uid=uid).first()
        # Modify Content
        _post.title = parse.unquote(header).lower().strip()
        _post.client = parse.unquote(subheader).lower().strip()
        _post.location = parse.unquote(location).lower().strip()
        _post.category = parse.unquote(category).lower().strip()
        _post.link = parse.unquote(link).strip()
        _post.custom_tags = parse.unquote(custom_tags).lower().strip()
        _post.custom_values = parse.unquote(custom_values).lower().strip()
        _post.save()
        # Standard Response
        return api.std(api.OK, f"\n[UPDATE] updating post content {_post}\n")
    except Exception as exception:
        # Unexpected Error Response
        return api.error(exception)


def attach_html(req, uid, *args, **kwargs):
    """
    Updates the specified record belonging to the given `uid` with new data

    :param content str: URIEncoded string containing html
    :return json: api.std
    """
    try:
        # Consume Input
        uid = parse.unquote(uid).strip()
        _post = Post.objects.get(uid=uid)
        if not hasattr(_post, "uid"):
            # Expected Error Response
            return api.error("\n[CLIENT INPUT ERROR] No post matching uid found.\n")
        else:
            # Modify Content
            _post.body = req.body.decode('utf-8')
            _post.save()
            # Standard Response
            return api.std(api.OK, f"\n[UPDATE] attaching new html to {_post}.\n")
    except Exception as exception:
        # Unexpected Error Response
        return api.error(exception)


def delete(req, uid, *args, **kwargs):
    """
    Purges all Post data related to uid

    :param uid str:
    :return bool: Which is true if the data was successfully purged
    """
    try:
        # Consume Input
        uid = parse.unquote(uid).strip()
        print('\n[DELETE] Attempting to remove Post:', uid, '\n')
        # Purge Related Data
        _post = Post.objects.filter(uid=uid)
        _post.delete()
        # Standard Success Response
        return api.std(message="Success!", status=api.OK)
    except Exception as exception:
        # Unexpected Error Response
        return api.error(exception)
