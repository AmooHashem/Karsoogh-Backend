from django.db import models
from django.utils.safestring import mark_safe

from karsoogh.settings import GRADE_CHOICE, CONTENT_TYPE


class BaseFieldsModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایشی')

    class Meta:
        abstract = True


class Province(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, verbose_name='کد')
    title = models.CharField(max_length=255, verbose_name='عنوان استان')

    def __str__(self):
        return self.title


class City(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, verbose_name='کد')
    title = models.CharField(max_length=255, verbose_name='عنوان شهر')
    province = models.ForeignKey('Province', on_delete=models.PROTECT, verbose_name='استان',
                                 related_name='city_province')

    def __str__(self):
        return self.title


class School(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, verbose_name='کد مدرسه')
    title = models.CharField(max_length=255, verbose_name='عنوان مدرسه')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='شهر', related_name='school_city')

    def __str__(self):
        return self.title


class Student(BaseFieldsModel):
    national_code = models.CharField(max_length=11, verbose_name='کد ملی')
    password = models.CharField(max_length=255, verbose_name='کلمه عبور')
    phone1 = models.CharField(max_length=11, verbose_name='تلفن همراه')
    phone2 = models.CharField(max_length=11, verbose_name='تلفن همراه دوم', null=True, blank=True)
    first_name = models.CharField(max_length=40, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(max_length=40, verbose_name='نام خانوادگی', null=True, blank=True)
    grade = models.IntegerField(choices=GRADE_CHOICE, verbose_name='پایه تحصیلی', null=True, blank=True)
    school_name = models.CharField(max_length=255, verbose_name='نام مدرسه', null=True, blank=True)
    school_phone = models.CharField(max_length=40, verbose_name='شماره تلفن مدرسه', null=True, blank=True)
    manager_name = models.CharField(max_length=40, verbose_name='نام مدیر مدرسه', null=True, blank=True)
    manager_phone = models.CharField(max_length=40, verbose_name='شماره مدیر مدرسه', null=True, blank=True)
    user_token = models.CharField(max_length=255, verbose_name='توکن', null=True, blank=True)
    expire_token = models.DateTimeField(verbose_name='انقضای توکن', null=True, blank=True)
    status = models.IntegerField(verbose_name='وضعیت', default=0)
    school = models.ForeignKey('School', on_delete=models.PROTECT, verbose_name='مدرسه',
                               related_name='student_school', null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='شهر',
                             related_name='student_city', null=True, blank=True)

    def __str__(self):
        return '{}|{} {}'.format(self.national_code, self.first_name, self.last_name)


class Payment(BaseFieldsModel):
    order_id = models.CharField(max_length=50, verbose_name='آی دی پرداخت')
    amount = models.IntegerField(verbose_name='مبلغ')
    name = models.CharField(max_length=255, verbose_name='نام پرداخت کننده')
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه')
    mail = models.CharField(max_length=255, verbose_name='پست الکترونیک', null=True, blank=True)
    desc = models.CharField(max_length=255, verbose_name='توضیح تراکنش')
    callback = models.CharField(max_length=2048, verbose_name='آدرس بازگشت')

    pay_id = models.CharField(max_length=255, unique=True, verbose_name='آی دی پرداخت', null=True, blank=True)
    pay_link = models.CharField(max_length=255, verbose_name='لینک پرداخت', null=True, blank=True)
    return_link = models.CharField(max_length=255, verbose_name='لینک بازگشت', null=True, blank=True)

    status = models.IntegerField(verbose_name='وضعیت تراکنش', null=True, blank=True)
    track_id = models.IntegerField(verbose_name='کد رهگیری آیدی پی', null=True, blank=True)
    card_no = models.CharField(max_length=255, verbose_name='شماره کارت پرداخت کننده با فرمت', null=True, blank=True)
    hashed_card_no = models.CharField(max_length=255, verbose_name='هش شماره کارت پرداخت کننده', null=True, blank=True)
    response_text = models.TextField(verbose_name='اطلاعات خام بازگشتی', null=True, blank=True)
    date = models.IntegerField(verbose_name='زمان پرداخت تراکنش', null=True, blank=True)

    student = models.ForeignKey('Student', on_delete=models.PROTECT, verbose_name='دانش آموز',
                                related_name='pay_student')

    def __str__(self):
        return mark_safe('{}</br>{}|{}'.format(self.student, self.status, self.order_id))


class PaymentResCode(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, verbose_name='کد')
    desc = models.CharField(max_length=255, verbose_name='شرح کد')
    status = models.IntegerField(verbose_name='وضعیت', null=True, blank=True)

    def __str__(self):
        return self.desc


class Exam(BaseFieldsModel):
    title = models.CharField(max_length=255, verbose_name='عنوان آزمون')
    holding_date = models.DateTimeField(verbose_name='تاریخ برگزاری', null=True, blank=True)
    ending_date = models.DateTimeField(verbose_name='تاریخ خاتمه', null=True, blank=True)
    status = models.IntegerField(verbose_name='وضعیت', default=0)

    def __str__(self):
        return self.title


class Question(BaseFieldsModel):
    title = models.CharField(max_length=255, verbose_name='عنوان سوال')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    status = models.IntegerField(verbose_name='وضعیت', default=0)
    exam = models.ForeignKey('Exam', on_delete=models.PROTECT, verbose_name='آزمون', related_name='question_exam')

    def __str__(self):
        return self.title[0:30]


class Content(BaseFieldsModel):
    title = models.CharField(max_length=255, verbose_name='عنوان محتوا')
    content = models.TextField(verbose_name='محتوا')
    content_type = models.IntegerField(choices=CONTENT_TYPE, verbose_name='نوع محتوا', default=1)
    status = models.IntegerField(verbose_name='وضعیت', default=0)

    def __str__(self):
        return self.title[0:30]


class QuestionContent(BaseFieldsModel):
    ordering = models.IntegerField(verbose_name='ترتیب', default=0)
    question = models.ForeignKey('Question', on_delete=models.PROTECT, verbose_name='سوال', related_name='qc_question')
    content = models.ForeignKey('Content', on_delete=models.PROTECT, verbose_name='محتوا', related_name='qc_content')
    status = models.IntegerField(verbose_name='وضعیت', default=0)

    def __str__(self):
        return mark_safe(self.content.title[0:30] + '<br>' + self.question.title[0:30])


class Answer(BaseFieldsModel):
    answer = models.TextField(verbose_name='جواب', null=True, blank=True)
    file = models.FileField(verbose_name='فایل', null=True, blank=True)
    question_content = models.ForeignKey('QuestionContent', on_delete=models.PROTECT, verbose_name='محتوای سوال',
                                         related_name='answer_qc')
    student = models.ForeignKey('Student', on_delete=models.PROTECT, verbose_name='دانش آموز',
                                related_name='answer_student')

    def __str__(self):
        return '{} {}'.format(self.student.first_name, self.student.last_name)
