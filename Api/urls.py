from django.urls import path
from Api import views

app_name = 'Api'



urlpatterns = [
    # path('', views.home, name='home'),
    # path('test/', views.test, name='test'),

    path('get/time/', views.get_time, name='get_time'),

    path('student/register/', views.create_account, name='create account'),
    path('student/register/completed/', views.register_complete, name='register_complete'),
    # todo: change to fill profile
    path('student/change/password/', views.change_password, name='change_password'),
    path('student/profile/', views.student_check, name='student_check'),
    path('student/login/', views.login, name='login'),
    path('student/logout/', views.logout, name='logout'),

    path('pay/request/', views.pay_request, name='pay_request'),  # todo: pay for each exam
    path('pay/submit/', views.pay_submit, name='pay_submit'),  # todo: submit for each exam
    path('pay/check/', views.pay_check, name='pay_check'),  # todo: check per exam
    path('pay/ignore/', views.pay_ignore, name='pay_ignore'),  # todo: remove

    path('province/', views.province, name='province'),
    path('city/', views.city, name='city'),
    path('city/detail/', views.get_city_details, name='get_city_details'),
    path('school/', views.school, name='school'),  # todo: from front, add school if does not exist

    path('exam/', views.get_student_exams, name='get exams of student'),
    path('exam/register/', views.register, name='register in exam'),
    path('exam/question/list/', views.get_question, name='get_question'),
    path('exam/question/<int:question_id>/content/', views.get_content, name='get_content'),
    path('exam/answer/', views.answer, name='answers'),
    path('exam/student/answer/<int:qc_id>/', views.get_student_content, name='get_student_content'),
    # sep added
    path('answer/show/', views.show_answer, name='show answer'),
    path('answer/set/', views.set_score, name='set score'),

    path('examstudent/sum_score/', views.sum_score, name='sum of scores'),
    path('examstudent/is_pass/', views.is_pass, name='check is pass'),
]
