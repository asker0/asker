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
	path('question/<int:question_id>', views.question, name='question'),
	path('answer/<int:answer_id>/like', views.like, name='like'),
	path('answer/<int:answer_id>/delete', views.delete_answer, name='delete_answer'),
	path('user/<str:username>', views.profile, name='profile'),
	path('ask', views.ask, name='ask'),
	path('signin', views.signin, name='signin'),
	path('signup', views.signup, name='signup'),
	path('logout', views.logout, name='logout'),
	path('test', views.test, name='test'),
	path('ads.txt', views.test, name='test'),
	path('notifications', views.notification, name='notification'),
	path('deleteQuestion', views.deleteQuestion, name='deleteQuestion'),
	path('comments', views.comments, name='comments'),
	path('comment', views.comment, name='comment'),
	path('rank', views.rank, name='rank'),
	path('response', views.edit_response, name='edit_response'),
	path('question/apagar/pergunta/moderador/apagar/<int:question_id>', views.delete_question, name='delete_question'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
