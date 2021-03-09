import json
import datetime
from django.http import HttpResponse

from Api.models import PaymentResCode
from karsoogh.settings import RESPONSE_TEMPLATE, SESSION_TIME


def get_response(res_code, data=None):
    if not data:
        data = {}
    payment_res_code = PaymentResCode.objects.filter(pk=res_code).first()
    if payment_res_code:
        status = payment_res_code.status
        if not status:
            status = 200
        return HttpResponse(json.dumps(RESPONSE_TEMPLATE.format(res_code, payment_res_code.desc, data)), status=status)
    else:
        return HttpResponse(json.dumps(RESPONSE_TEMPLATE.format(res_code, "no_message", data)), status=403)


def get_expire_time():
    return datetime.datetime.now() + datetime.timedelta(0, 0, 0, 0, SESSION_TIME)


def timestamp(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.timestamp()
