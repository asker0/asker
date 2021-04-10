from django.contrib import admin

from .models import Question, Response, Comment

admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Comment)
