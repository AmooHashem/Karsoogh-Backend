from django.urls import path
from Api import views

app_name = 'Api'

urlpatterns = [
       # path('', views.home, name='home'),
       # path('test/', views.test, name='test'),

       path('get/time/', views.get_time, name='get_time'),

       path('student/register/', views.register, name='register'),
       path('student/register/completed/', views.register_complete, name='register_complete'),
       path('student/change/password/', views.change_password, name='change_password'),
       path('student/profile/', views.student_check, name='student_check'),
       path('student/login/', views.login, name='login'),
       path('student/logout/', views.logout, name='logout'),

       path('pay/request/', views.pay_request, name='pay_request'),
       path('pay/submit/', views.pay_submit, name='pay_submit'),
       path('pay/check/', views.pay_check, name='pay_check'),
       path('pay/ignore/', views.pay_ignore, name='pay_ignore'),

       path('province/', views.province, name='province'),
       path('city/', views.city, name='city'),
       path('city/detail/', views.get_city_details, name='get_city_details'),
       path('school/', views.school, name='school'),
       path('students/', views.students, name='students'),

       path('exam/question/list/', views.get_question, name='get_question'),
       path('exam/question/<int:question_id>/content/', views.get_content, name='get_content'),
       path('exam/answer/', views.answer, name='answers'),
       path('exam/student/answer/<int:qc_id>/', views.get_student_content, name='get_student_content'),
       # sep added
       path('answer/<int:ans_id>/', views.answershow, name='show answer'),
       path('answer/set/<int:ans_id>/<int:_score>/', views.set_score, name='set score'),
       path('examstudent/sum_score/<int:exam_student_id>', views.sum_score, name='sum of scores'),
       path('examstudent/is_pass/<int:exam_student_id>', views.is_pass, name='check is pass'),
]
