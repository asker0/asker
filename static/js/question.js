$(document).ready(function() {
	$('.navbar-light .dmenu').hover(function() {
		$(this).find('.sm-menu').first().stop(true, true).slideDown(150);
	}, function() {
		$(this).find('.sm-menu').first().stop(true, true).slideUp(105);
	});
});

function anti_spam(obj) {
	if (obj.parentElement.response.value == '') {
		alert('Preencha sua resposta.')
		return false
	}

	return true
}

function show_more(obj) {
	obj.style.display = 'none'
	obj.nextSibling.style.display = 'inline'
	obj.nextSibling.nextSibling.nextSibling.style.display = 'inline'
}

function show_less(obj) {
	obj.style.display = 'none'
	obj.previousSibling.previousSibling.style.display = 'none'
	obj.previousSibling.previousSibling.previousSibling.style.display = 'inline'
}

function report(response_id, obj) {
	// quando a denúncia tiver sido feita, a função abaixo é executada:
	function ok() {
		obj.parentElement.innerHTML = '<p>Resposta denunciada com sucesso <i class="far fa-check-circle"></i></p>'
		obj.remove()
	}
	
	$.ajax({
		type: 'get',
		url: '/report',
		data: {
			type: 'response',
			id: response_id,
		},
		
		complete: function () {
			ok()
		}
	})
}

function report_question(question_id, obj) {
	// quando a denúncia tiver sido feita, a função abaixo é executada:
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
