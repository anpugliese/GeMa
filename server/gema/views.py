from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from django.template import loader
from django.http import HttpResponse
from .models import Choice, Question
import json

@csrf_exempt
def geoids(request):
    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        lat = body["latitude"]
        lng = body['longitude'] 
        h = body['h']
        #lat = request.POST['latitude']
        #lng = request.POST['longitude'] 
        #h = request.POST['h']
        
        res = json.dumps({"lat": lat, "lng": lng, "h": h})
    return HttpResponse(res, status=200)


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'gema/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'gema/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'gema/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'gema/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('gema:results', args=(question.id,)))