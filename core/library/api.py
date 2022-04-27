# Django library
from django.conf import settings
from django.http import JsonResponse

# Overlord library
from .console import Console

OK = 'OK'
BAD = 'BAD'
CON = Console()


def std(status, message="Invalid Status Response"):
    """
    Standard API Response Method

    :param status (OK/BAD): api.OK or api.BAD type
    :param message dict: contains api response data
    :return dict: {status, message}
    """
    if isinstance(message, Exception):
        message = str(message)
    return JsonResponse({
        'status': status,
        'data': message,
    })


def error(exception=None):
    """
    Internal server error standard response method

    :return: api.std showing a HTTP 500 Error
    """
    if exception is not None:
        print(f"""
            [{CON.output("API ERROR 500", "red")}]
        """)
        print(exception, "\n")
    return std(BAD, "Error 500: internal server error")


def table(Table, Headers, Body, filter={ "order_by": str() }):
    """
    Create a API for Populating Tables Method

    :param Table model: Model class to fetch data from
    :param headers list: list of strings containing table headers which you want to fetch and return
    return dict: api.std response
    """
    row_count = Table.objects.count()

    if row_count >= 1:

        if row_count > 100:
            row_count = 100

        body_query = Table.objects.filter().order_by(filter['order_by'])[:row_count]
        body_row_data = Body(body_query)

        return std(OK, {
            'head': Headers,
            'body': body_row_data
        })

    return std(OK, {'head': [], 'body': [ [] ]})
