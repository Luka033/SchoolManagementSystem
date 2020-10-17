from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Students_Course)
admin.site.register(Department)
# admin.site.register(Major)

# class MajorAdmin(admin.ModelAdmin):
#     raw_id_fields = ('required_courses', 'electives',)
#
#     class Meta:
#         def __str__(self):
#             return self.course_id


admin.site.register(Major)



