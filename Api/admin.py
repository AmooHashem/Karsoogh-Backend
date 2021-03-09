from django.contrib import admin

# Register your models here.
from Api.models import *

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(PaymentResCode)
admin.site.register(School)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Content)
admin.site.register(QuestionContent)
admin.site.register(Answer)