from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe

from karsoogh.settings import PROBLEM_STATUS, PROBLEM_SUBJECTS, GAME_MODE, GRADE


class BaseFieldsModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایشی')

    class Meta:
        abstract = True


class Student(BaseFieldsModel):
    national_id = models.CharField(max_length=10, verbose_name='کد ملی', primary_key=True)
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه', null=True)
    name = models.CharField(max_length=40, verbose_name='نام و نام‌خانوادگی', null=True)

    def __str__(self):
        return '{} | {}'.format(self.national_id, self.name)


class Team(BaseFieldsModel):
    id = models.CharField(verbose_name='شناسه', max_length=100, primary_key=True)
    voice_chat_link = models.CharField(verbose_name='لینک چت صوتی', max_length=255, null=True)
    name = models.CharField(max_length=40, verbose_name='نام')
    grade = models.IntegerField(choices=GRADE, null=True)
    student1 = models.ForeignKey('Student', on_delete=models.PROTECT, verbose_name='نفر اول',
                                 related_name='first_member')
    student2 = models.ForeignKey('Student', on_delete=models.PROTECT, verbose_name='نفر دوم',
                                 related_name='second_member')
    student3 = models.ForeignKey('Student', on_delete=models.PROTECT, verbose_name='نفر سوم',
                                 related_name='third_member')
    score = models.IntegerField(verbose_name='امتیاز', default=0)

    def __str__(self):
        return '{} | {} | {}'.format(self.student1.name, self.student2.name, self.student3.name)


class Problem(BaseFieldsModel):
    text = models.TextField(verbose_name='متن')
    subject = models.IntegerField(choices=PROBLEM_SUBJECTS, verbose_name='موضوع', null=True)

    def __str__(self):
        return PROBLEM_SUBJECTS[self.subject][1]


class ProblemTeam(BaseFieldsModel):
    problem = models.ForeignKey('Problem', on_delete=models.PROTECT, verbose_name='مسئله')
    team = models.ForeignKey('Team', on_delete=models.PROTECT, verbose_name='تیم')
    score = models.IntegerField(verbose_name='نمره', default=0)
    status = models.IntegerField(choices=PROBLEM_STATUS, verbose_name='وضعیت', default=0)
    answer = models.TextField(verbose_name='پاسخ', null=True)


class Game(BaseFieldsModel):
    mode = models.CharField(choices=GAME_MODE, verbose_name='حالت', max_length=40)


class PaymentResCode(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, verbose_name='کد')
    desc = models.CharField(max_length=255, verbose_name='شرح کد')
    status = models.IntegerField(verbose_name='وضعیت', null=True, blank=True)

    def __str__(self):
        return self.desc

# class Question(BaseFieldsModel):
#     title = models.CharField(max_length=255, verbose_name='عنوان سوال')
#     description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
#     status = models.IntegerField(verbose_name='وضعیت', default=0)
#     exam = models.ForeignKey('Exam', on_delete=models.PROTECT, verbose_name='آزمون', related_name='question_exam')
#
#     def __str__(self):
#         return self.title[0:30]
#

# class Answer(BaseFieldsModel):
#     answer = models.TextField(verbose_name='جواب', null=True, blank=True)
#     file = models.FileField(verbose_name='فایل', null=True, blank=True)
#     question_content = models.ForeignKey('QuestionContent', on_delete=models.PROTECT, verbose_name='محتوای سوال',
#                                          related_name='answer_qc')
#     student = models.ForeignKey('Student', on_delete=models.PROTECT, verbose_name='دانش آموز',
#                                 related_name='answer_student')
#     score = models.IntegerField(default=0, verbose_name='نمره')
#     comment = models.TextField(verbose_name='نظر مصحح', blank=True, null=True)
#
#     def __str__(self):
#         return '{} {}'.format(self.student.first_name, self.student.last_name)
