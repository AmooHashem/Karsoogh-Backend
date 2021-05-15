from django.contrib import admin

# Register your models here.
from Formula0.models import *

admin.site.register(Student)
admin.site.register(Team)
admin.site.register(Problem)
admin.site.register(ProblemTeam)
