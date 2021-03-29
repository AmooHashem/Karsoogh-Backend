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


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    # def get_qc_id(self, obj):
    #     return obj.question_content.id

    def csv_download(self, request, queryset):
        import csv
        from django.http import HttpResponse
        file = open('answer.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(['id', 'qc_id'])
        for i in queryset:
            writer.writerow([i.id, i.question_content.id])

        file.close()

        f = open('answer.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=answer.csv'
        return response

    list_display = ('id', 'question_content_id', 'student')
    actions = [csv_download]


admin.site.register(ExamStudent)