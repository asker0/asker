"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main_app import views

urlpatterns = [
	path('', views.index, name='index'),
	path('news', views.index, name='index'),
	path('popular', views.index, name='index'),
	path('question/<int:question_id>', views.question, name='question'),
	path('answer/like', views.like, name='like'),
	path('delete_response', views.delete_response, name='delete_response'),
	path('user/<str:username>', views.profile, name='profile'),
	path('user/<str:username>/edit', views.edit_profile, name='edit_profile'),
	path('user/<str:username>/block', views.block, name='block'),
	path('ask', views.ask, name='ask'),
	path('signin', views.signin, name='signin'),
	path('signup', views.signup, name='signup'),
	path('logout', views.logout, name='logout'),
	path('test', views.test, name='test'),
	path('notifications', views.notification, name='notification'),
	path('delete_question', views.deleteQuestion, name='deleteQuestion'),
	path('delete_comment', views.delete_comment, name='delete_comment'),
	path('comments', views.comments, name='comments'),
	path('comment', views.comment, name='comment'),
	path('rank', views.rank, name='rank'),
	path('edit-response', views.edit_response, name='edit_response'),
	path('get_more_questions', views.get_more_questions, name='get_more_questions'),
	path('get_more_responses', views.get_more_responses, name='get_more_responses'),
	path('report', views.report, name='report'),
	path('account/verify', views.account_verification, name='account_verification'),
	path('user/<str:username>/info', views.user_info, name='user_info'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
