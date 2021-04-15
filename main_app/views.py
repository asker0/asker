from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User

from main_app.models import UserProfile, Question, Response, Notification, Comment, Report

from main_app.forms import UploadFileForm

from bs4 import BeautifulSoup as bs

import random, string

def index(request):
	if request.method == 'POST':
		Response.objects.create(question=Question.objects.get(id=request.POST.get('question_id')),
								creator=UserProfile.objects.get(user=request.user),
								text=request.POST.get('response'))
		u = UserProfile.objects.get(user=request.user)
		u.total_points += 2
		u.save()
		return HttpResponse('OK')

	all = Question.objects.all().order_by('-pub_date')
	p = Paginator(all, 20)

	page = request.GET.get('page', 1)

	context = {'questions': p.page(page).object_list,
			   'page_obj': p.page(page),
			   'new_questions_display': request.GET.get('nqd', 'block'),
			   'popular_questions_display': request.GET.get('pqd', 'none'),
			   'popular_tab': ' disabled',
			   'new_tab': ' active'}

	if request.GET.get('nqd', False):
		context['new_tab'] = ' active'
		context['popular_tab'] = ' disabled'
		context['popular_questions_display'] = 'none'

	# contexto das questões populares:
	context['popular_questions'] = sorted(p.page(1).object_list, key=lambda x:x.total_likes, reverse=True)

	return render(request, 'index.html', context)


def question(request, question_id):

	try:
		q = Question.objects.get(id=question_id)
	except:
		# pergunta não encontrada:
		return HttpResponse('''<html>
			<head>
				<meta charset="utf-8">
				<meta name="viewport" content="width=device-width, initial-scale=1">
			</head>
			<body>
				<p>Essa pergunta não existe, talvez ela tenha sido apagada pelo criador da pergunta. <a href="/">Clique aqui</a> para voltar para a página inicial.</p>
			</body>
			</html>''')

	if request.method == 'POST':
		if Response.objects.filter(creator=UserProfile.objects.get(user=request.user), question=Question.objects.get(id=question_id)).exists():
			return redirect('/question/' + str(q.id))

		if Response.objects.filter(question=q, creator=UserProfile.objects.get(user=request.user)).exists():
			return redirect('/question/' + str(q.id))

		r = Response.objects.create(question=q, creator=UserProfile.objects.get(user=request.user), text=request.POST.get('response'))

		u = UserProfile.objects.get(user=request.user)
		u.total_points += 2
		u.save()

		# cria a notificação da resposta:
		n = Notification.objects.create(receiver=r.question.creator.user,
										type='question-answered')
		n.set_text(r.id)
		n.save()

		return HttpResponse(r.id)

	context = {'question': q,
			   'responses': Response.objects.filter(question=q).order_by('-pub_date').order_by('-total_likes')}

	if not request.user.is_anonymous:
		context['user_p'] = UserProfile.objects.get(user=request.user)
		context['answered'] = Response.objects.filter(creator=UserProfile.objects.get(user=request.user), question=q).exists()

	return render(request, 'question.html', context)


def like(request, answer_id):

    r = Response.objects.get(id=answer_id)

    if r.likes.filter(username=request.user.username).exists():
        r.likes.remove(request.user)
        r.total_likes -= 1
        r.save()
    else:
        r.likes.add(request.user)
        r.total_likes += 1
        r.save()

        # cria uma notificação para o like (quem recebeu o like será notificado):
        n = Notification.objects.create(receiver=Response.objects.get(id=answer_id).creator.user,
                                        type='like-in-response')
        n.set_text(answer_id)
        n.save()

        # aumenta total de likes da pergunta:
        q = r.question
        q.total_likes += 1
        q.save()

    return HttpResponse('OK')


def delete_answer(request, answer_id):
    r = Response.objects.get(id=answer_id)
    r.delete()
    return HttpResponse('OK')


def signin(request):

	r = request.GET.get('redirect')

	if r == None:
		r = '/'

	if request.method == 'POST':
		r = request.POST.get('redirect')
		email = request.POST.get('email')
		password = request.POST.get('password')

		# testa se o email existe:
		if not User.objects.filter(email=email).exists():
			return render(request, 'signin.html', {'login_error': '''<div class="alert alert-danger" role="alert">Dados de login incorretos.</div>''',
												   'redirect': r})

		user = authenticate(username=User.objects.get(email=email).username, password=password)

		if user is None:
			return render(request, 'signin.html', {'login_error': '''<div class="alert alert-danger" role="alert">Dados de login incorretos.</div>''',
												   'redirect': r})
		login(request, user)
		return redirect(r)

	return render(request, 'signin.html', {'redirect': r})


def signup(request):

	if request.method == 'POST':
		r = request.POST.get('redirect')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')

		if User.objects.filter(username=username).exists():
			return render(request, 'signup.html', {'error': '''<div class="alert alert-danger" role="alert">Nome de usuário em uso.</div>''',
												   'username': username,
												   'email': email,
												   'redirect': r})

		if User.objects.filter(email=email).exists():
			return render(request, 'signup.html', {'error': '''<div class="alert alert-danger" role="alert">Email em uso.</div>''',
												   'username': username,
												   'email': email,
												   'redirect': r})

		u = User.objects.create_user(username=username.strip(), email=email.strip(), password=password)
		login(request, u)

		UserProfile.objects.create(user=u)

		return redirect(r)

	context = {
		'redirect': request.GET.get('redirect', '/'),
	}

	return render(request, 'signup.html', context)


def profile(request, username):

	context = {'user_p': UserProfile.objects.get(user=User.objects.get(username=username)),
			   'change_profile_picture_form': UploadFileForm()}

	if request.user.username == username:
		context['questions'] = Paginator(Question.objects.filter(creator=UserProfile.objects.get(user=request.user)).order_by('-pub_date'), 4).page(1).object_list
		context['responses'] = Paginator(Response.objects.filter(creator=UserProfile.objects.get(user=request.user)).order_by('-pub_date'), 4).page(1).object_list

	if request.method == 'POST':

		new_bio = request.POST.get('bio', None)

		if new_bio != None:
			u = UserProfile.objects.get(user=request.user)
			u.bio = new_bio
			u.save()
			return redirect('/user/' + username)

		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			f = request.FILES['file']

			file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			file_name += str(f)

			with open('django_project/media/avatars/' + file_name, 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)

			u = UserProfile.objects.get(user=request.user)
			u.avatar = 'avatars/' + file_name
			u.save()

			return redirect('/user/' + request.user.username)

	return render(request, 'profile.html', context)


def ask(request):

	if request.method == 'POST':

		if request.POST.get('question') == '' or request.POST.get('question') == '.':
			return render(request, 'ask.html', {'error': '<p>Pergunta inválida.</p>'})

		description = bs(request.POST.get('description'), 'html.parser').text
		text = bs(request.POST.get('question'), 'html.parser').text

		q = Question.objects.create(creator=UserProfile.objects.get(user=request.user), text=text, description=description)

		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			f = request.FILES['file']

			file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			file_name += str(f)

			with open('django_project/media/questions/' + file_name, 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
			q.image = 'questions/' + file_name
			q.save()

		u = UserProfile.objects.get(user=request.user)
		u.total_points += 1
		u.save()

		return redirect('/question/' + str(q.id))

	return render(request, 'ask.html')


def logout(request):
	django_logout(request)
	return redirect('/')


def test(request):
	return render(request, 'test.html')


def notification(request):

    p = Paginator(Notification.objects.filter(receiver=request.user).order_by('-creation_date'), 15)

    page = request.GET.get('page', 1)

    context = {
        'notifications': p.page(page),
    }

    return render(request, 'notification.html', context)


def deleteQuestion(request):
	if request.method != 'POST':
		return HttpResponse('Erro.')
	q = Question.objects.get(id=request.POST.get('question_id'))
	q.delete()
	return HttpResponse('OK')


def comments(request):
	response_id = request.POST.get('response_id')
	page = request.POST.get('page')

	json = {}

	# testa se existem ou não comentários para está pergunta
	if not Comment.objects.filter(response=Response.objects.get(id=response_id)).exists():
		json['has_comments'] = 'false'
		return JsonResponse(json)

	json['has_coments'] = 'true'
	'''
	json['comments'] = {
		'foo': {'username': 'teste', 'image_url': '/media/avatars/7EQMG6PQJYunnamed%20(1).jpg', 'comment': 'eu não concordo com você porque papapa'},




	}'''

	p = Paginator(Comment.objects.filter(response=Response.objects.get(id=response_id)).order_by('pub_date'), 3)

	comments = p.page(page).object_list

	id_list = []
	for c in comments.all():
		id_list.append(c.id)

	json['total_comments'] = len(comments)

	if len(Comment.objects.filter(id__in=id_list)) == 1:
		json['comments'] = {
			1: {
				'username': Comment.objects.filter(id__in=id_list).first().creator.username,
				'image_url': UserProfile.objects.get(user=Comment.objects.filter(id__in=id_list).first().creator).avatar.url,
				'comment': Comment.objects.filter(id__in=id_list).first().text,
				'id': Comment.objects.filter(id__in=id_list).first().id,
			}
		}
	elif len(Comment.objects.filter(id__in=id_list)) == 2:
		json['comments'] = {
			1: {
				'username': Comment.objects.filter(id__in=id_list).first().creator.username,
				'image_url': UserProfile.objects.get(user=Comment.objects.filter(id__in=id_list).first().creator).avatar.url,
				'comment': Comment.objects.filter(id__in=id_list).first().text,
				'id': Comment.objects.filter(id__in=id_list).first().id,
			},

			2: {
				'username': Comment.objects.filter(id__in=id_list).last().creator.username,
				'image_url': UserProfile.objects.get(user=Comment.objects.filter(id__in=id_list).last().creator).avatar.url,
				'comment': Comment.objects.filter(id__in=id_list).last().text,
				'id': Comment.objects.filter(id__in=id_list).last().id,
			},
		}
	else:
		json['comments'] = {
			1: {
				'username': Comment.objects.filter(id__in=id_list).first().creator.username,
				'image_url': UserProfile.objects.get(user=Comment.objects.filter(id__in=id_list).first().creator).avatar.url,
				'comment': Comment.objects.filter(id__in=id_list).first().text,
				'id': Comment.objects.filter(id__in=id_list).first().id,
			},

			2: {
				'username': Comment.objects.filter(id__in=id_list)[1].creator.username,
				'image_url': UserProfile.objects.get(user=Comment.objects.filter(id__in=id_list)[1].creator).avatar.url,
				'comment': Comment.objects.filter(id__in=id_list)[1].text,
				'id': Comment.objects.filter(id__in=id_list)[1].id,
			},
			3: {
				'username': Comment.objects.filter(id__in=id_list).last().creator.username,
				'image_url': UserProfile.objects.get(user=Comment.objects.filter(id__in=id_list).last().creator).avatar.url,
				'comment': Comment.objects.filter(id__in=id_list).last().text,
				'id': Comment.objects.filter(id__in=id_list).last().id,
			},
		}

	# calcula se tem outra página de comentários desta resposta:
	if p.page(page).has_next():
		json['has_next'] = 'true'
	else:
		json['has_next'] = 'false'

	return JsonResponse(json)


def comment(request):
	if request.method != 'POST':
		return HttpResponse('ERROR.')

	response_id = request.POST.get('response_id')
	text = request.POST.get('comment')

	r = Response.objects.get(id=response_id)

	c = Comment.objects.create(response=r, creator=request.user, text=text)


	n = Notification.objects.create(receiver=r.creator.user, type='comment-in-response')
	n.set_text(r.id, comment_id=c.id)
	n.save()

	return redirect('/question/' + request.POST.get('question_id'))


def rank(request):
	p = Paginator(UserProfile.objects.all().order_by('-total_points'), 50)
	r = p.page(1)
	count = 1
	for u in r:
		u.rank = count
		count += 1
	context = {'rank': r}
	return render(request, 'rank.html', context)


def edit_response(request):

	r = Response.objects.get(creator=UserProfile.objects.get(user=request.user), id=request.POST.get('response_id'))
	r.text = request.POST.get('response')
	r.save()

	return redirect('/question/' + str(r.question.id))


def get_more_questions(request):
	q = Question.objects.filter(creator=UserProfile.objects.get(user=request.user)).order_by('-pub_date')
	p = Paginator(q, 4)
	page = request.POST.get('q_page', 2)

	json = {
	}

	json['questions'] = {}

	count = 1
	for q in p.page(page):
		json['questions'][count] = {
			'text': q.text,
			'id': q.id,
		}
		count += 1

	if not p.page(page).has_next():
		json['has_next'] = 'false'

	return JsonResponse(json)


def get_more_responses(request):
	r = Response.objects.filter(creator=UserProfile.objects.get(user=request.user)).order_by('-pub_date')
	p = Paginator(r, 4)
	page = request.POST.get('r_page', 2)

	json = {
	}

	json['responses'] = {}

	count = 1
	for r in p.page(page):
		json['responses'][count] = {
			'text': r.text,
			'question_text': r.question.text,
			'id': r.question.id,
		}
		count += 1

	if not p.page(page).has_next():
		json['has_next'] = 'false'

	return JsonResponse(json)


def delete_question(request, question_id):
	q = Question.objects.get(id=question_id)
	q.delete()
	return HttpResponse('OK')


def delete_comment(request):
	c = Comment.objects.get(id=request.POST.get('comment_id'))
	c.delete()
	return HttpResponse('OK')


def report(request):
	if request.GET.get('type') == 'response':
		if Report.objects.filter(item=request.GET.get('id')).exists():
			return HttpResponse('OK')

		if request.user.is_anonymous:
			reporter = None
		else:
			reporter = request.user

		Report.objects.create(type=request.GET.get('type'),
							  item=request.GET.get('id'),
							  reporter=reporter)
	return HttpResponse('OK')


def edit_profile(request, username):
	
	if request.method == 'POST':
		if request.POST.get('type') == 'profile-pic':
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				f = request.FILES['file']
				file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
				file_name += str(f)
				
				with open('django_project/media/avatars/' + file_name, 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)
				u = UserProfile.objects.get(user=request.user)
				u.avatar = 'avatars/' + file_name
				u.save()
			return redirect('/user/' + username)
		if request.POST.get('type') == 'bio':
			u = UserProfile.objects.get(user=request.user)
			u.bio = request.POST.get('bio')
			u.save()
			return redirect('/user/' + username)
		if request.POST.get('type') == 'username':
			
			if User.objects.filter(username=request.POST.get('username')).exists():
				return render(request, 'edit-profile.html', {'user_p': UserProfile.objects.get(user=User.objects.get(username=username)), 'username_display': 'block', 'invalid_username': ' is-invalid'})
			
			password = request.POST.get('password')
			user = authenticate(username=request.user.username, password=password)
			if user is None:
				if not User.objects.filter(username=request.POST.get('username')).exists():
					return render(request, 'edit-profile.html', {'user_p': UserProfile.objects.get(user=User.objects.get(username=username)), 'password_display': 'block', 'invalid_password': ' is-invalid'})
			user.username = request.POST.get('username')
			user.save()
			login(request, user)
			return redirect('/user/' + user.username)
	
	return render(request, 'edit-profile.html', {'user_p': UserProfile.objects.get(user=User.objects.get(username=username))})
