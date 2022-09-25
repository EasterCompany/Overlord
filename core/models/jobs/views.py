# Standard library
import re
import json
from uuid import uuid1
from urllib import parse
# Overlord library
from core.library import api, time
from core.models.jobs.tables import JobPost


def list_all(req, *args, **kwargs):
    """
    Returns a list of all Title, Client, Location, Salary & Timestamp combinations within the database

    [   ["Title", "Client" ... ] <-- Table Headers
        [[], [],  [], []   ... ] <-- Table Row & Data ]

    formated for use with a table to be presented like this (below):

    H1          H2          H3
    -------     -------     -------
    ..          ..          ..
    ..          ..          ..
    """

    def __body__(body_query):
        """
        Contains instructions on how to generate the table content for the front end application

        :param body_query querySet: django query set
        :return json: api table
        """
        body_row_data = []

        for job in body_query:
            body_row_data.append([
                str(job),
                str(job.title).title(),
                str(job.client).title(),
                str(job.location).title(),
                int(job.min_salary),
                int(job.max_salary),
                str(job.datestamp())
            ])

        return body_row_data

    # Return Table Response
    return api.table(
        Table=JobPost,
        Headers=['UID', 'Title', 'Client', 'Location', '(Min) Salary', '(Max) Salary', 'Date'],
        Body=__body__,
        filter={ "order_by": "datetime" }
    )


def get(req, uid, *args, **kwargs):
    """
    Returns a dictionary of job data

    :param uid str: unique identifier
    :return: api.std
    """

    # Consume Input
    uid = parse.unquote(uid)

    # Fetch Data
    try:
        post = JobPost.objects.filter(uid=uid).first()
    except Exception as exception:
        return api.std(
            status=api.BAD,
            message={'error': str(exception)}
        )
    posted = str(post.datetime).split(' ')[0].split('-')

    # Return Standard Response
    return api.std(
        status=api.OK,
        message={
            'uid': str(post.uid),
            'title': str(post.title).title(),
            'client': str(post.client).title(),
            'location': str(post.location).title(),
            'info': str(post.info),
            'min_salary': int(post.min_salary),
            'max_salary': int(post.max_salary),
            'timestamp': f"{posted[2]}/{posted[1]}/{posted[0]}",
            'applications': post.applications
        }
    )


def create(req, title, client="", location="Remote", min_salary=0, max_salary=0, *args, **kwargs):
    """
    Create a new Job Post

    :param title str:
    :param client str:
    :param location str:
    :param min_salary int:
    :param max_salary int:
    :return json: api.std
    """

    # Consume Input
    uid = uuid1()
    title = parse.unquote(title).lower().strip()
    client = parse.unquote(client).lower().strip()
    location = parse.unquote(location).lower().strip()
    min_salary = re.sub(r'[a-z]', '', parse.unquote(min_salary).lower()).strip()
    max_salary = re.sub(r'[a-z]', '', parse.unquote(max_salary).lower()).strip()

    # Create Job
    try:
        JobPost.objects.create(
            uid=uid,
            datetime=time.get_datetime_str(),
            title=title,
            client=client,
            location=location,
            min_salary=min_salary,
            max_salary=max_salary
        )
    except Exception as exception:
        return api.error(exception)

    # Return Standard Response
    return api.std(message=uid, status=api.OK)


def update(req, uid, title, client="", location="Remote", min_salary=0, max_salary=0, *args, **kwargs):
    """
    Updates the specified record belonging to the given `uid` with new data

    :param title str:
    :param client str:
    :param location str:
    :param min_salary int:
    :param max_salary int:
    :return json: api.std
    """

    # Consume Input
    j = JobPost.objects.filter(uid=uid).first()

    # Modify Content
    j.title = parse.unquote(title).lower().strip()
    j.client = parse.unquote(client).lower().strip()
    j.location = parse.unquote(location).lower().strip()
    j.min_salary = re.sub(r'[a-z]', '', parse.unquote(min_salary).lower()).strip()
    j.max_salary = re.sub(r'[a-z]', '', parse.unquote(max_salary).lower()).strip()
    j.save()

    # Return Standard Response
    return api.std(message="Success!", status=api.OK)


def attach_html(req, uid, *args, **kwargs):
    """
    Updates the specified record belonging to the given `uid` with new HTML data

    :param uid str: URIEncoded string containing JobPost uuid
    :return json: api.std
    """
    try:
        # Consume Input
        uid = parse.unquote(uid).strip()
        _job = JobPost.objects.get(uid=uid)
        if not hasattr(_job, "uid"):
            # Expected Error Response
            return api.error("\n[CLIENT INPUT ERROR] No JobPost matching uid found.\n")
        else:
            # Modify Content
            _job.info = req.body.decode('utf-8')
            _job.save()
            # Standard Response
            return api.std(api.OK, f"\n[UPDATE] attaching new html to JobPost ({_job}).\n")
    except Exception as exception:
        # Unexpected Error Response
        return api.error(exception)


def attach_application(req, uid, fname, lname, email, tel, *args, **kwargs):
    """
    Updates the specified record belonging to the given `uid` with new Application data

    :param uid str: URIEncoded string containing JobPost uid
    :param fname str: URIEncoded string containing user first name
    :param lname str: URIEncoded string containing user last name
    :param email str: URIEncoded string containing user email address
    :param tel str: URIEncoded string containing user telephone number
    :return json: api.std
    """
    try:
        # Consume Input
        uid = parse.unquote(uid).strip()
        email = parse.unquote(email).strip()
        fname = parse.unquote(fname).strip()
        lname = parse.unquote(lname).strip()
        _job = JobPost.objects.get(uid=uid)
        if not hasattr(_job, "uid"):
            # Expected Error Response
            return api.error("\n[CLIENT ERROR] No JobPost matching uid found.\n")
        else:
            if email in _job.applications:
                # Expected Error Response
                return api.error("\n[CLIENT ERROR] User has already applied.\n")
            # Modify Content
            _job.applications[email] = {
                'fname': fname,
                'lname': lname,
                'tel': tel,
                'checked': False
            }
            print(_job.applications[email])
            _job.save()
            print("SAVED!")
            # Standard Response
            return api.std(
                api.OK,
                f"\n[UPDATE] attaching new application to JobPost {_job}\n"
            )
    except Exception as exception:
        # Unexpected Error Response
        return api.error(exception)


def delete(req, uid, *args, **kwargs):
    """
    Purges all Job Post data related to uid

    :param uid str:
    :return bool: Which is true if the data was successfully purged
    """
    # Consume Input
    uid = parse.unquote(uid).strip()
    print('\n[DELETE] JobPost:', uid, '\n')

    # Purge Related Data
    try:
        _job = JobPost.objects.filter(uid=uid)
        _job.delete()
    except Exception as exception:
        return api.error(exception)

    # Return Standard Response
    return api.std(message="success", status=api.OK)
