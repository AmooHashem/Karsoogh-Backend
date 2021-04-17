from django.http import HttpResponse
from django.contrib import admin
from Api.models import *
import csv

# Register your models here.

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(PaymentResCode)
admin.site.register(School)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Question)
admin.site.register(Content)
admin.site.register(QuestionContent)
admin.site.register(ExamStudent)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    def download_csv(self, request, queryset):
        file = open('answer.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(['id', 'qc_id'])
        for answer in queryset:
            writer.writerow([answer.id, answer.question_content.id])
        file.close()

        f = open('answer.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=answer.csv'
        return response

    list_display = ('id', 'question_content_id', 'student')
    download_csv.short_description = 'Export Selected as csv'
    actions = [download_csv]


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    def temporary(self, request, queryset):
        pass

    def set_exam_participants(self, request, queryset):
        pass

    def sum_scores(self, request, queryset):
        answers = list(Answer.objects.all())
        students = list(Student.objects.all())
        for selected_exam in queryset:
            for student in students:
                exam_student = ExamStudent.objects.filter(exam=selected_exam, student=student)
                if len(exam_student) == 0:
                    ExamStudent.objects.create(exam=selected_exam, student=student)
                else:
                    exam_student[0].score = 0
                    exam_student[0].save()

            for answer in answers:
                answer_exam = answer.question_content.question.exam
                if selected_exam != answer_exam:
                    continue
                student = answer.student
                exam_student = ExamStudent.objects.get(exam=selected_exam, student=student)
                print(answer.score)
                exam_student.score = exam_student.score + answer.score
                exam_student.save()

    def get_student_info_csv(self, request, queryset):
        file = open('answer.csv', 'w')
        writer = csv.writer(file)
        students = list(Student.objects.all())
        first_row = ['کد ملی', 'نام', 'نام خانوادگی', 'پایه', 'مدرسه', 'شهر', 'استان']
        for exam in queryset:
            first_row.append(exam.title)
        writer.writerow(first_row)
        for student in students:
            if not student.city or not student.grade:  # todo: fix in a better way! (for example, have a is_valid function)
                continue
            row = [student.national_code, student.first_name, student.last_name, student.grade, student.school_name,
                   student.city.title, student.city.province.title]
            for exam in queryset:
                exam_student = ExamStudent.objects.get(exam=exam, student=student)
                row.append(exam_student.score)
            writer.writerow(row)
        file.close()

        f = open('result.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=result.csv'
        return response

    set_exam_participants.short_description = \
        'تعیین شرکت‌کنندگان در آزمون‌های انتخاب‌شده (تنها در صورتی که آزمون‌های انتخابی بدون هزینه باشند)'
    sum_scores.short_description = 'جمع‌زدن نمرات دانش‌آموزان در آزمون‌های انتخاب‌شده (این فرآیند زمان‌بر است!)'
    get_student_info_csv.short_description = 'دریافت فایل اکسل نمرات دانش‌آموزان در آزمون‌های انتخاب‌شده'
    temporary.short_description = 'موقت (تعیین شرکت‌کنندگان آزمون اول)'
    actions = [sum_scores, get_student_info_csv, set_exam_participants, temporary]
