from django.core.management import BaseCommand

from Api.models import ExamStudent, Exam, Student
import os


class Command(BaseCommand):
    help = 'create ExamStudent by exam and student name'

    def handle(self, *args, **options):
        query_exam = list(Exam.objects.all())
        query_student = list(Student.objects.all())
        for exam in query_exam:
            for student in query_student:
                ExamStudent.objects.create(
                    exam=exam,
                    student=student,
                    can_register=True,
                    is_preregister=True,
                    is_register_complete=True,
                )
                print('ExamStudent created')