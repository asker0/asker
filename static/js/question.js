function like(likeElement, response_id) {
	
	/* alterna a imagem do like (se coração vermelho, então fica coração branco, e vice-versa) */
	like_image = likeElement.getElementsByTagName('img')[0]
	if (like_image.src[like_image.src.length - 11] == 'e') { /* se o coração for branco */
		like_image.src = '/static/images/red-heart.png'
		
		/* aumenta o total de likes do contador */
		span_like_counter = likeElement.getElementsByTagName('span')[0]
		span_like_counter.innerHTML = Number(span_like_counter.innerHTML) + 1
	}
	else {
		like_image.src = '/static/images/white-heart.png'
		
		/* diminuí o total de likes do contador */
		span_like_counter = likeElement.getElementsByTagName('span')[0]
		span_like_counter.innerHTML = Number(span_like_counter.innerHTML) - 1
	}
	
	$.ajax({
		url: '/answer/like',
		data: {
			answer_id: response_id,
		},
		complete: function() {
			return
		}
	})
}

function show_comments(commentsDiv, response_id, commentsIcon, csrf_token, user_logged, question_id) {
	
	commentsSection = commentsDiv.getElementsByClassName('comments')[0]
	
	if (commentsSection.getElementsByTagName('form')[0] != undefined) {
		commentsSection.getElementsByTagName('form')[0].remove()
	}
	
	if (commentsSection.getElementsByClassName('load-more')[0] != undefined) {
		commentsSection.getElementsByClassName('load-more')[0].remove()
	}
	
	$.ajax({
		url: '/comments',
		data: {
			id: response_id,
			page: commentsSection.id,
		},
		complete: function(data) {
			data = JSON.parse(data.responseText)
			$.each(data.comments, function(index, value) {
				if(user_logged != value.username) {
					commentsSection.innerHTML += '<div class="c"><hr><a style="text-decoration: none; color: black;" href="/user/'+value.username+'"><img src="'+value.avatar+'" width="40px"> <span>'+value.username+'</span></a><p>'+value.text+'</p><hr></div>'
				} else {
					commentsSection.innerHTML += '<div class="c"><hr><a style="text-decoration: none; color: black;" href="/user/'+value.username+'"><img src="'+value.avatar+'" width="40px"> <span>'+value.username+'</span></a> <img onclick="delete_comment('+value.comment_id+'); this.parentElement.remove()" style="float: right; cursor: pointer;" width="20px" src="/static/images/trash.png"> <p>'+value.text+'</p><hr></div>'
				}
			})
			
			if(data.has_next) {
				commentsSection.id = Number(commentsSection.id) + 1
				
				/* Adiciona elemento para clicar e carregar mais comentários */
				commentsSection.innerHTML += `<p class="load-more" onclick="show_comments(this.parentElement.parentElement, ${response_id}, this.parentElement.getElementsByTagName('img')[0], '${csrf_token}', '`+user_logged+`', `+question_id+`)">Carregar mais</p>`
			}
			
			/* Adiciona o formulário para comentar */
			commentsSection.innerHTML += '<form class="form-inline" method="post" action="/comment"><input type="hidden" name="csrfmiddlewaretoken" value="'+csrf_token+'"><input type="hidden" name="response_id" value="'+response_id+'">  <input type="hidden" name="question_id" value="'+question_id+'">  <textarea maxlength="400" class="form-control" name="text" placeholder="Escreva seu comentário"></textarea><input class="btn btn-outline-primary" type="submit" value="Pronto"></form>'
		}
	})
	
	commentsIcon.onclick = function() {
		var el = commentsDiv.getElementsByClassName('comments')[0]
		var styleObj;

		if (typeof window.getComputedStyle != "undefined") {
			styleObj = window.getComputedStyle(el, null);
		} else if (el.currentStyle != "undefined") {
			styleObj = el.currentStyle;
		}

		if (styleObj) {
		   if(styleObj.display == 'block') {
			   el.style.display = 'none'
		   } else {
			   el.style.display = 'block'
		   }
		}
	}
}

function delete_response(response_id) {
	$.ajax({
		url: '/delete_response',
		data: {
			response_id: response_id,
		},
		complete: function() {
			alert('Resposta apagada.')
		}
	})
}

function delete_comment(comment_id, csrf_token) {
	$.ajax({
		url: '/delete_comment',
		type: 'get',
		data: {
			comment_id: comment_id,
		},
		complete: function() {
			alert('Comentário deletado.')
		}
	})
}

function report_question(question_id, obj) {
	// quando a denÃºncia tiver sido feita, a funÃ§Ã£o abaixo Ã© executada:
	function ok() {
		obj.parentElement.innerHTML = '<p>Pergunta denunciada com sucesso <i class="far fa-check-circle"></i></p>'
		obj.remove()
	}
	
	$.ajax({
		type: 'get',
		url: '/report',
		data: {
			type: 'question',
			id: question_id,
		},
		
		complete: function () {
			ok()
		}
	})
}

$(function () {
	$('[data-toggle="popover"]').popover({
		container: 'body',
		html: true,
		title: 'Denunciar abuso',
	})
})
