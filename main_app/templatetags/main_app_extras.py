from django import template

from main_app.models import User, UserProfile, Question, Response, Comment

register = template.Library()

@register.filter(name='answered')
def answered(username, question_id):
	if Response.objects.filter(creator=UserProfile.objects.get(user=User.objects.get(username=username)), question=Question.objects.get(id=question_id)).exists():
		return True
	return False


@register.filter(name='answer')
def answer(username, question_id):
	try:
		text = Response.objects.get(creator=UserProfile.objects.get(user=User.objects.get(username=username)), question=Question.objects.get(id=question_id)).text
	except:
		text = 'null'
	if len(text) > 77:
		text = text[0:77] + '...'
	return text


@register.filter(name='total_answers')
def total_answers(question_id):
	try:
		return Response.objects.filter(question=Question.objects.get(id=question_id)).count()
	except:
		return ''


@register.filter(name='total_likes')
def total_likes(response_id):
    return Response.objects.get(id=response_id).likes.all().count()


@register.filter(name='like_or_not')
def like_or_not(response_id, username):
    r = Response.objects.get(id=response_id)

    if r.likes.filter(username=username).exists():
        return 'red-heart.png'
    return 'white-heart.png'


@register.filter(name='total_comments')
def total_comments(response_id):
    return Comment.objects.filter(response=Response.objects.get(id=response_id)).count()


@register.filter(name='last_response_pub_date')
def last_response_pub_date(question_id):
    q = Question.objects.get(id=question_id)
    return Response.objects.filter(question=q).order_by('-pub_date')[0].pub_date


@register.filter(name='last_response')
def last_response(question_id):
	from django.contrib.humanize.templatetags.humanize import naturaltime
	try:
		r = Response.objects.filter(question=Question.objects.get(id=question_id)).order_by('-pub_date')
		return 'respondida {} por <a href="/user/{}">{}</a>'.format(naturaltime(r[0].pub_date), r[0].creator.user.username, r[0].creator.user.username)
	except:
		return ''
