from django.contrib import admin
from .models import Task, SendTask, Comment

admin.site.register(Task)
admin.site.register(SendTask)
admin.site.register(Comment)
