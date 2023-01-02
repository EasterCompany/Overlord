# TODO: Deprecated file needs removed

# Framework imports
from django.http import JsonResponse
# Local imports
from .admin import BAD_status, OK_status,upgrade_request


def status_code(status=BAD_status):
    return JsonResponse({'status': status})


def OLT_upgrade_request_api(req, *args, **kwargs):
    status = BAD_status
    if 'secret' in req.headers:
        status = upgrade_request(req.headers['secret'])
    return status_code(status)


def OLT_status_api(req, *args, **kwargs):
    return status_code(OK_status)
