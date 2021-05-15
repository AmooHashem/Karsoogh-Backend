import json
from django.http import HttpResponse

from karsoogh.settings import NEW_RESPONSE_TEMPLATE


def get_response(message, data=None, status=200):
    if data is None:
        data = {}
    return HttpResponse(json.dumps(NEW_RESPONSE_TEMPLATE.format(message, data)), status=status)


def get_problem_cost(subject):
    if subject % 2 == 0:
        return 1
    return 2
