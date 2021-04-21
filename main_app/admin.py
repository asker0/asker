from django.contrib import admin

from .models import UserProfile, Question, Response, Comment, Report, Ban

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Ban)
