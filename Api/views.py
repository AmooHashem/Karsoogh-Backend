import json
import uuid
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
from django.db.models import Avg, Sum, Min, Max

from Api.decorators import check_token
from Api.forms import AnswerForm
from Api.functions import get_response, get_expire_time, timestamp
from Api.models import Payment, Student, PaymentResCode, Province, City, School, Question, QuestionContent, Answer, \
    ExamStudent, Exam
from karsoogh.settings import API_TOKEN, SANDBOX


def get_time(request):
    return HttpResponse(json.dumps('{"message": "' + str(datetime.now().timestamp()) + '", "status": true }'),
                        status=200)


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            post_data = request.POST
            national_code = post_data.get('national_code')
            password = post_data.get('password')
            phone1 = post_data.get('phone1')
            if Student.objects.filter(national_code=national_code).count() > 0:
                return get_response(664)
            token = uuid.uuid4().hex
            student = Student(national_code=national_code, password=make_password(password), phone1=phone1,
                              user_token=token, expire_token=get_expire_time())
            student.save()
            return get_response(61, '{{"token": "{}"}}'.format(token))
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
@check_token
def register_complete(request):
    if request.method == "POST":
        try:
            post_data = request.POST
            phone2 = post_data.get('phone2')
            first_name = post_data.get('first_name')
            last_name = post_data.get('last_name')
            school_name = post_data.get('school_name')
            school_phone = post_data.get('school_phone')
            manager_name = post_data.get('manager_name')
            manager_phone = post_data.get('manager_phone')
            grade = post_data.get('grade')
            city = post_data.get('city')
            school = post_data.get('school')
            request.student.phone2 = phone2
            request.student.first_name = first_name
            request.student.last_name = last_name
            request.student.school_name = school_name
            request.student.school_phone = school_phone
            request.student.manager_name = manager_name
            request.student.manager_phone = manager_phone
            request.student.grade = int(grade)
            request.student.city_id = int(city)
            # request.student.school = int(school)
            request.student.save()
            return get_response(64)
        except Exception as ex:
            return get_response(600, '"{}"'.format(ex))
    return get_response(601)


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            post_data = request.POST
            national_code = post_data.get('national_code')
            password = post_data.get('password')
            student = Student.objects.filter(national_code=national_code).first()
            if student:
                if not check_password(password, student.password):
                    return get_response(660)
                token = uuid.uuid4().hex
                student.user_token = token
                student.expire_token = get_expire_time()
                student.save()
                return get_response(60, '{{"token": "{}"}}'.format(token))
            else:
                return get_response(660)
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
def change_password(request):
    if request.method == "POST":
        try:
            post_data = request.POST
            national_code = post_data.get('national_code')
            phone1 = post_data.get('phone1')
            new_password = post_data.get('new_password')
            student = Student.objects.filter(national_code=national_code, phone1=phone1).first()
            if student:
                student.password = make_password(new_password)
                token = uuid.uuid4().hex
                student.user_token = token
                student.expire_token = get_expire_time()
                student.save()
                return get_response(68, '{{"token": "{}"}}'.format(token))
            else:
                return get_response(668)
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
def logout(request):
    if request.method == "GET":
        try:
            token = request.headers.get('Token')
            student = Student.objects.filter(user_token=token).first()
            if student:
                student.expire_token = datetime.now()
                student.save()
                return get_response(63)
            else:
                return get_response(662)
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
@check_token
def pay_request(request):
    if request.method == "POST":
        data = request.POST
        amount = int(data.get('amount'))
        return_link = data.get('return_link')
        mail = data.get('mail')
        student = request.student

        name = student.first_name + ' ' + student.last_name if student.first_name else student.national_code
        phone = student.phone1
        desc = name + '|' + phone

        order_id = '1'
        while Payment.objects.filter(order_id=order_id).count() > 0:
            rand = random.randint(2, 10)
            order_id = str(Payment.objects.all().order_by('-pk')[0].pk + rand)
        payment = Payment(student=student, order_id=order_id, amount=amount, name=name, phone=phone, mail=mail,
                          desc=desc, return_link=return_link, status=0)
        payment.save()
        payload = {
            'order_id': order_id,
            'amount': amount,
            'name': name,
            'phone': phone,
            'mail': mail,
            'desc': desc,
            # 'callback': 'http://127.0.0.1:8000/pay/submit/'.format(request.headers.get('host'))
            'callback': 'https://{}/pay/submit/'.format(request.headers.get('host'))
        }
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_TOKEN,
            'X-SANDBOX': SANDBOX,
        }
        r = requests.post('https://api.idpay.ir/v1.1/payment', data=json.dumps(payload), headers=headers)
        status = r.status_code
        if status == 201:
            pay_id = json.loads(r.text).get('id')
            pay_link = json.loads(r.text).get('link')
            data = '{{"pay_link": "{}"}}'.format(pay_link)
            payment.pay_id = pay_id
            payment.pay_link = pay_link
            payment.save()
        else:
            json_res = json.loads(r.text)
            data = '{{"error_code": "{}", "error_message": "{}"}}'.format(
                json_res.get('error_code'),
                json_res.get('error_message')
            )
        return get_response(200, data)
    else:
        return get_response(601)


# todo: should be removed
@csrf_exempt
@check_token
def pay_ignore(request):
    if request.method == "GET":
        student = request.student
        if student.status != 10 or student.status != 20:
            student.status = 20
            student.save()
            return get_response(62)
        else:
            return get_response(665)
    else:
        return get_response(601)


def get_city_details(request):
    if request.method == "GET":
        try:
            province = request.headers.get('province')
            city = request.headers.get('city')
            if province:
                pr = Province.objects.filter(pk=int(province)).first()
                return get_response(62, '{{"id": {}, "title": "{}"}}'.format(pr.pk, pr.title))
            elif city:
                ct = City.objects.filter(pk=int(city)).first()
                return get_response(62, '{{"id": {}, "title": "{}", "pid": "{}", "province": "{}"}}'
                                    .format(ct.pk, ct.title, ct.province.pk, ct.province.title))
            else:
                return get_response(665)
        except Exception as ex:
            return get_response(600, '"{}"'.format(ex))
    else:
        return get_response(601)


@csrf_exempt
def pay_submit(request):
    if request.method == "POST":
        data = request.POST
        error_code = data.get('error_code')
        status = data.get('status')
        payment = Payment.objects.filter(order_id=data.get('order_id')).first()

        token = payment.student.user_token
        pay_status = -1
        if payment.status == 0:
            payment.status = int(status)
            payment.track_id = data.get('track_id')
            # payment.pay_id = data.get('id')
            # amount = data.get('amount')
            payment.card_no = data.get('card_no')
            payment.hashed_card_no = data.get('hashed_card_no')
            payment.date = int(data.get('date'))
            payment.save()

            payload = {
                'id': payment.pay_id,
                'order_id': payment.order_id,
            }
            headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': API_TOKEN,
                'X-SANDBOX': SANDBOX,
            }
            r = requests.post('https://api.idpay.ir/v1.1/payment/verify', data=json.dumps(payload), headers=headers)
            status = r.status_code
            payment.status = status
            payment.save()

            try:
                payment.response_text = r.text
                json_load = json.loads(r.text)
                pay_status = int(json_load.get('status'))
                payment.status = pay_status
                payment.save()

                payment.student.status = 10 if pay_status == 100 or pay_status == 101 else 1
                payment.student.expire_token = get_expire_time()
                payment.student.save()
            except:
                pay_status = json.loads(r.text).get('status')
                if pay_status is None:
                    pay_status = -2
        if status:
            _redirect = redirect(payment.return_link + '?status={}&token={}&q={}'.format(status, token, pay_status))
        else:
            _redirect = redirect(payment.return_link + '?error_code={}&token={}'.format(error_code, token))
        # _redirect = redirect(payment.return_link)
        # _redirect['status'] = status
        # _redirect['token'] = token
        return _redirect
    return get_response(601)


@csrf_exempt
@check_token
def pay_check(request):
    if request.method == "GET":
        payments = list(request.student.pay_student.all().values('order_id', 'amount', 'desc', 'status', 'update_date'))
        return get_response(62, json.dumps(payments, default=timestamp))
    return get_response(601)


@csrf_exempt
@check_token
def student_check(request):
    if request.method == "GET":
        return get_response(62, serializers.serialize('json', [request.student, ]))
    return get_response(601)


@csrf_exempt
def students(request):
    if request.method == "GET":
        if request.GET.get('keygen') == 'c89fpg20xtg92c5110322':
            data = list(Student.objects.all().values(
                'id', 'national_code', 'phone1', 'phone2', 'first_name', 'last_name',
                'grade', 'school_name', 'school_phone', 'manager_name', 'manager_phone',
                'status', 'city', 'city__province'))
            return get_response(62, serializers.serialize('json', data))
    return get_response(601)


@csrf_exempt
def province(request):
    if request.method == "GET":
        return get_response(62, json.dumps(list(Province.objects.all().values('id', 'title'))))
    return get_response(601)


@csrf_exempt
def city(request):
    if request.method == "GET":
        p_id = request.headers.get('Province')
        return get_response(62, json.dumps(list(City.objects.filter(province_id=p_id).values('id', 'title'))))
    return get_response(601)


@csrf_exempt
def school(request):
    if request.method == "GET":
        c_id = request.headers.get('City')
        return get_response(62, json.dumps(list(School.objects.filter(city_id=c_id).values('id', 'title'))))
    return get_response(601)


# @csrf_exempt
# def test(request):
#     payload = {
#         'amount': 2000,
#         'name': 'Student',
#         'phone': '09123456789',
#         'mail': 'mail@test.com',
#         'desc': 'تست پرداخت',
#     }
#     # r = requests.get('http://backend.interkarsolar.ir/get/time')
#     r = requests.post('http://backend.interkarsolar.ir/pay/request', data=json.dumps(payload))
#     r = requests.post('http://127.0.0.1:8000/pay/request', data=json.dumps(payload))
#     # payload = {
#     #     'national_code': '1234567890',
#     #     'password': '123',
#     #     'phone': '09123456789',
#     # }
#     # r = requests.post('http://127.0.0.1:8000/student/register/', data=json.dumps(payload))
#     return HttpResponse(r.content)
#
#
# def home(request):
#     r = render(request, 'test.html')
#     # data = [
#     #     [64,    "حساب کاربری با موفقیت بروز شد",    202],
#     # ]
#     # for d in data:
#     # #     prc = PaymentResCode.objects.filter(pk=660)
#     # #     prc.status = 401
#     # #     prc = PaymentResCode.objects.filter(pk=660)
#     # #     prc.status = 401
#     # #     prc.save()
#     #     pr = PaymentResCode(id=d[0], desc=d[1], status=d[2])
#     #     pr.save()
#     return r

@csrf_exempt
@check_token
def get_student_exams(request):
    if request.method != "GET":
        return get_response(601)
    student = request.student
    exam_students = ExamStudent.objects.filter(student=student)
    result = []
    for exam_student in exam_students:
        result.append({
            'status': exam_student.status,
            'id': exam_student.exam.id,
            'title': exam_student.exam.title,
            'start_date': exam_student.exam.start_date,
            'finish_date': exam_student.exam.finish_date,
            'registration_start': exam_student.exam.registration_start,
            'registration_deadline': exam_student.exam.registration_deadline,
            'registration_description': exam_student.exam.registration_description,
            'cost': exam_student.exam.cost,
        })
    return get_response(62, json.dumps(result, default=str))


@csrf_exempt
@check_token
def register(request):
    if request.method != "POST":
        return get_response(601)
    exam_id = request.POST.get('exam_id')
    student = request.student
    exam_student = ExamStudent.objects.get(exam__id=exam_id, student=student)
    exam = exam_student.exam
    if exam.cost == 0 or exam.prerequisite:
        exam_student.status = 1
        exam_student.save()
    else:
        pass  # todo
    return get_response(62)


@csrf_exempt
@check_token
def get_question(request):
    if request.method != "POST":
        return get_response(601)

    exam_id = request.POST.get('exam_id')
    exam = get_object_or_404(Exam, id=exam_id)
    if exam.start_date.timestamp() < datetime.now().timestamp() < exam.finish_date.timestamp():
        return get_response(62, json.dumps(list(Question.objects.filter(exam_id=exam_id, status=1).values('id'))))
    else:
        return get_response(800)


@csrf_exempt
@check_token
def get_content(request, question_id):
    if request.method == "POST":
        try:
            q = Question.objects.filter(pk=question_id).first()
            qc = q.qc_question.filter(status=1, content__status=1) \
                .annotate(qc_id=F('pk'), type=F('content__content_type'), title=F('content__title'),
                          content_desc=F('content__content')).order_by('ordering')
            data = '{{ "title": "{}", "description": "{}", "contents": {} }}' \
                .format(q.title, q.description, json.dumps(list(qc.values('qc_id', 'type', 'title', 'content_desc'))))
            return get_response(62, data)
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
@check_token
def get_student_content(request, qc_id):
    if request.method == "POST":
        try:
            ans = Answer.objects.filter(question_content_id=qc_id, student=request.student).first()
            if ans:
                data = '{{ "answer": "{}", "file": "{}" }}'.format(ans.answer, ans.file)
                return get_response(62, data)
            else:
                return get_response(602)
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
@check_token
def answer(request):
    if request.method == "POST":
        try:
            qc_id = request.POST.get('qc_id')
            instance = Answer.objects.filter(question_content_id=qc_id, student=request.student).first()
            form = AnswerForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                with transaction.atomic():
                    if instance and request.POST.get('new_set') == 'true':
                        instance.delete()
                    f = form.save(commit=False)
                    f.question_content_id = qc_id
                    f.student = request.student
                    if request.FILES.get('file') and request.POST.get('answer'):
                        f.save()
                        res_code = 67
                    elif request.FILES.get('file'):
                        f.save()
                        res_code = 65
                    elif request.POST.get('answer'):
                        f.save()
                        res_code = 66
                    elif request.POST.get('new_set') == 'true':
                        res_code = 69
                    else:
                        res = get_response(667)
                        transaction.set_rollback(True)
                        return res
                    return get_response(res_code, '{{"answer_id": {}}}'.format(f.pk))
            return get_response(666)
        except Exception as d:
            return get_response(600)
    return get_response(601)


@csrf_exempt
def show_answer(request):
    if request.method == "POST":
        ans_id = request.POST.get('ans_id')
        ans = get_object_or_404(Answer, id=ans_id)
        data = '{{"text": "{}", "answer_text": "{}", "answer_file": "{}", "comment": "{}"}}' \
            .format(ans.question_content.question, ans.answer, ans.file, ans.comment)
        return get_response(62, data)
    return get_response(601)


@csrf_exempt
def set_score(request):
    if request.method == "POST":
        ans_id = request.POST.get('ans_id')
        score = request.POST.get('score')
        comment = request.POST.get('comment')
        student_answer = get_object_or_404(Answer, id=ans_id)
        if score is not None:
            student_answer.score = score
        student_answer.comment = comment
        student_answer.save()
        return get_response(62)
    return get_response(601)


@csrf_exempt
@check_token
def sum_score(request):
    if request.method == "POST":
        exam_id = request.POST.get('exam_id')
        student = request.student
        exam_student = ExamStudent.objects.get(exam__id=exam_id, student=student)
        # ans = 0
        # print('salam1')
        exam_stu = ExamStudent.objects.get(id=exam_student.id)
        # print('salam12')
        query = Answer.objects.filter(student=exam_stu.student,
                                      question_content__question__exam__id=exam_stu.exam.id).aggregate(ans=Sum('score'))
        # print('salam123')
        # data = '{{ "sum_score" : {} }}'.format(ans)
        return get_response(62, query)
    return get_response(601)


@csrf_exempt
@check_token
def is_pass(request):
    # print('hello')
    if request.method == "POST":
        # print('enterTheF')
        exam_id = request.POST.get('exam_id')
        student = request.student
        exam_student = ExamStudent.objects.get(exam__id=exam_id, student=student)
        exam_stu = ExamStudent.objects.get(id=exam_student.id)
        query = Answer.objects.filter(student=exam_stu.student,
                                      question_content__question__exam__id=exam_stu.exam.id).aggregate(ans=Sum('score'))

        if query['ans'] >= exam_stu.exam.min_score:
            datat = '{{ "pass": True }}'
            exam_stu.is_pass = True
            exam_stu.save()
            return get_response(62, datat)
        else:
            dataf = '{{ "pass": False }}'
            return get_response(62, dataf)
    return get_response(601)
