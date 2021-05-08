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


class AnswersListFilterByNationalCode(admin.SimpleListFilter):
    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Student National Code'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'national_code'

    default_value = None

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # filter_list = []
        # queryset = Student.objects.all()
        # for student in queryset:
        #     filter_list.append(
        #         (student.national_code, f'{student.first_name} {student.last_name} | {student.national_code}')
        #     )
        return [('123456789',
                 'با کلیک بر روی این گزینه، جواب‌های دانش‌آموز با کد ملی ۱۲۳۴۵۶۷۸۹ نمایش داده میشه (که منطقاً خالیه!) حالا شما می‌تونید توی آدرس به جای ۱۲۳۴۵۶۷۸۹، هر کد ملی‌ای رو که می‌خواید، بذارید!')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(student__national_code=self.value())
        return queryset

    # def value(self):
    #     """
    #     Overriding this method will allow us to always have a default value.
    #     """
    #     value = super(AnswersListFilter, self).value()
    #     if value is None:
    #         if self.default_value is None:
    #             # If there is at least one Species, return the first by name. Otherwise, None.
    #             first_species = Answer.objects.order_by('student__national_code').first()
    #             value = None if first_species is None else first_species.id
    #             self.default_value = value
    #         else:
    #             value = self.default_value
    #     return str(value)


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
    list_filter = (AnswersListFilterByNationalCode,)
    download_csv.short_description = 'Export Selected as csv'
    actions = [download_csv]


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    def set_exam_participants(self, request, queryset):
        for selected_exam in queryset:
            if not selected_exam.prerequisite:
                continue

            selected_exam_students = ExamStudent.objects.filter(exam=selected_exam)
            for selected_exam_student in selected_exam_students:
                selected_exam_student.delete()

            for prerequisite_exam_student in ExamStudent.objects.filter(exam=selected_exam.prerequisite):
                if prerequisite_exam_student.status == 2:
                    new_exam_student = \
                        ExamStudent(exam=selected_exam, student=prerequisite_exam_student.student, status=0)
                    new_exam_student.save()

    def set_exam_final_result(self, request, queryset):
        for selected_exam in queryset:
            all_answers = list(Answer.objects.all())
            answers = []
            for answer in all_answers:
                if answer.question_content.question.exam == selected_exam:
                    answers.append(answer)

            for exam_student in ExamStudent.objects.filter(exam=selected_exam):
                exam_student.score = 0
                exam_student.save()

            for answer in answers:
                student = answer.student
                exam_student = ExamStudent.objects.get(exam=selected_exam, student=student)
                exam_student.score = exam_student.score + answer.score
                exam_student.save()

            for exam_student in ExamStudent.objects.filter(exam=selected_exam):
                if exam_student.score >= selected_exam.required_score:
                    exam_student.status = 2
                else:
                    exam_student.status = 3
                exam_student.save()

    def get_student_info_csv(self, request, queryset):
        if len(queryset) > 1:
            return
        selected_exam = queryset[0]
        selected_exam_students = ExamStudent.objects.filter(exam=selected_exam)
        answers_of_selected_exam = []
        for answer in Answer.objects.all():
            if answer.question_content.question.exam == selected_exam:
                answers_of_selected_exam.append(answer)

        file = open('students.csv', 'w')
        writer = csv.writer(file)
        first_row = ['شناسه', 'کد ملی', 'نام', 'نام خانوادگی', 'شماره تلفن', 'شماره تلفن زاپاس', 'پایه', 'مدرسه',
                     'شماره تلفن مدرسه', 'شهر', 'استان', 'نام مدیر', 'شماره تلفن مدیر', 'وضعیت', 'تعداد پاسخ ارسال‌شده',
                     'نمره']
        writer.writerow(first_row)

        for selected_exam_student in selected_exam_students:
            student = selected_exam_student.student
            submitted_answers_count = 0
            for answer in answers_of_selected_exam:
                if answer.student == student:
                    submitted_answers_count += 1
            row = [student.id, student.national_code, student.first_name, student.last_name, student.phone1,
                   student.phone2, student.grade, student.school_name, student.school_phone,
                   student.city.title if student.city else '', student.city.province.title if student.city else '',
                   student.manager_name, student.manager_phone, STUDENT_EXAM_STATUS[selected_exam_student.status][1],
                   submitted_answers_count, selected_exam_student.score]
            writer.writerow(row)

        file.close()
        f = open('students.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=students.csv'
        return response

    set_exam_participants.short_description = \
        'تعیین شرکت‌کنندگان اولیه در آزمون‌های انتخاب‌شده (تنها در صورتی که آزمون‌های انتخابی بدون هزینه باشند)'
    set_exam_final_result.short_description = \
        'جمع‌زدن نمرات و تعیین پذیرفته‌شدگان در آزمون‌های انتخاب‌شده (این فرآیند زمان‌بر است!)'
    get_student_info_csv.short_description = \
        'دریافت فایل اکسل اطلاعات دانش‌آموزان در آزمون انتخاب‌شده (فقط یک آزمون انتخاب شود!)'
    actions = [set_exam_final_result, get_student_info_csv, set_exam_participants]
    list_display = ('id', 'title')
