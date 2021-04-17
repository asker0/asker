questions = document.getElementById("questions")
responses = document.getElementById("responses")
questions_section = document.getElementById("questions-section")
responses_section = document.getElementById("responses-section")

questions.onclick = function() {
	questions.classList.add("active")
	questions.classList.remove("disabled")
	
	responses.classList.add("disabled")
	responses.classList.remove("active")
	
	questions_section.style.display = "block"
	responses_section.style.display = "none"
}

responses.onclick = function() {
	questions.classList.add("disabled")
	questions.classList.remove("active")
	
	responses.classList.add("active")
	responses.classList.remove("disabled")
	
	questions_section.style.display = "none"
	responses_section.style.display = "block"
}


q_page = 1
function show_more_questions(button) {
	questions = document.getElementById('qs')
	
	$.ajax({
		type: 'get',
		dataType: 'json',
		url: '/get_more_questions',
		data: {
			q_page: ++q_page,
		},
		complete: function(data) {
			data = JSON.parse(data.responseText)
			
			$.each(data.questions, function(i, val) {
				questions.innerHTML += '<hr><div class="question"><a href="/question/'+val.id+'">'+val.text+'</a> <span>&middot; perguntada '+val.naturalday+'</span></div><hr>'
			})
			
			if(!data.has_next) {
				button.remove()
			}
		}
	})
}


r_page = 1
function show_more_responses(button) {
	responses = document.getElementById('rs')
	
	$.ajax({
		type: 'get',
		dataType: 'json',
		url: '/get_more_responses',
		data: {
			r_page: ++r_page,
		},
		complete: function(data) {
			data = JSON.parse(data.responseText)
			
			$.each(data.responses, function(i, val) {
				responses.innerHTML += '<hr><div class="response"><a href="/question/'+val.question_id+'">'+val.question_text+'</a><br><p>'+val.text+'</p></div><hr>'
			})
			
			if(!data.has_next) {
				button.remove()
			}
		}
	})
}
