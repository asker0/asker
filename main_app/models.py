from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='avatars/default-avatar.png')
	bio = models.TextField(max_length=400)
	total_points = models.IntegerField(null=True, default=0)

	rank = models.IntegerField(default=-1, null=True, blank=True)

	def __str__(self):
		return self.user.username

	def total_questions(self):
		return Question.objects.filter(creator=self).count()

	def total_responses(self):
		return Response.objects.filter(creator=self).count()

	def points(self):
		total = self.total_responses() * 2
		total += self.total_questions()
		return total


class Question(models.Model):
	creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	text = models.TextField()
	pub_date = models.DateTimeField(default=timezone.now)
	image = models.ImageField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
	    return self.text
	
	def cut_description(self):
		d = self.description[:300]
		
		if len(d) == 300 and len(self.description) > 300:
			d += '<span style="color: #007bff; cursor: pointer;" onclick="show_more(this)">...Mostrar mais</span><span style="display: none;">{}</span> <span style="color: #007bff; cursor: pointer; display: none;" onclick="show_less(this)">Mostrar menos</span>'.format(self.description[300:])
		
		return d


class Response(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	text = models.TextField()
	pub_date = models.DateTimeField(default=timezone.now)
	likes = models.ManyToManyField(User)
	total_likes = models.IntegerField(default=0)

	def __str__(self):
	    return self.text


class Comment(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Notification(models.Model):
	receiver = models.ForeignKey(User, on_delete=models.CASCADE)
	type = models.TextField() # tipos: question-answered, like-in-response, comment-in-response
	text = models.TextField(null=True)
	creation_date = models.DateTimeField(default=timezone.now)

	def set_text(self, answer_id, comment_id=None):
		if self.type == 'like-in-response':
			self.text = '<p>Você recebeu um ❤️ na sua resposta <a href="/question/{}">"{}"</a></p>'.format(Response.objects.get(id=answer_id).question.id, Response.objects.get(id=answer_id).text)
		if self.type == 'question-answered':
		    response = Response.objects.get(id=answer_id)
		    self.text = '<p><a href="/user/{}">{}</a> respondeu sua pergunta <a href="/question/{}">"{}"</a></p>'.format(response.creator.user.username, response.creator.user.username, response.question.id, response.question.text)
		if self.type == 'comment-in-response':
			comment = Comment.objects.get(response=Response.objects.get(id=answer_id), id=comment_id)
			self.text = '<p><a href="/user/{}">{}</a> comentou na sua resposta na pergunta: <a href="/question/{}">"{}"</a></p>'.format(comment.creator.username, comment.creator.username, comment.response.question.id, comment.response.question.text)
