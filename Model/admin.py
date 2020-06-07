from django.contrib import admin
from Model.models import student, course, comment, join, favor

# Register your models here.
admin.site.register([student, course, comment, join, favor])
