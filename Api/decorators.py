from datetime import datetime

from Api.functions import get_response, get_expire_time
from Api.models import Student


def check_token(func):
    def wrapped_func(request, *args, **kwargs):
        try:
            token = request.headers.get('Token')
            if not token:
                return get_response(601)
            student = Student.objects.filter(user_token=token).first()
            if not student or not student.expire_token:
                return get_response(662)
            elif student and student.expire_token.timestamp() < datetime.now().timestamp():
                return get_response(661)
            student.expire_token = get_expire_time()
            student.save()
            request.student = student
            return func(request, *args, **kwargs)
        except Exception as ex:
            return get_response(600, '"{}"'.format(ex))

    return wrapped_func
