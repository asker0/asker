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
	text = Response.objects.get(creator=UserProfile.objects.get(user=User.objects.get(username=username)), question=Question.objects.get(id=question_id)).text
	if len(text) > 77:
		text = text[0:77] + '...'
	return text


@register.filter(name='total_answers')
def total_answers(question_id):
    q = Question.objects.get(id=question_id)
    total = Response.objects.filter(question=q).count()

    if total == 0 or total > 1:
        return '<span id="total-answers-{}">'.format(q.id) + str(total) + '</span> <span id="total-answers-{}-text">respostas</span>'.format(q.id)
    return '<span id="total-answers-{}">1</span> resposta'.format(q.id)


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
