from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# FLAW #1: CSRF. This combined with the missing CSRF-token in the template detail.html disables Django's CSRF mitigations for this view.
# FIX #1: Comment out @csrf_exempt and include the csrf_token in the detail.html. 
# CSRF protection then automatically handled by middleware
@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class SearchResultsView(generic.ListView):
    model = Question
    template_name = 'polls/search.html'

    def get_queryset(self):
        query = self.request.GET['search_text']
        object_list = Question.objects.filter(question_text__icontains = query)
        return object_list

# FLAW #2: SQL injection. This whole view/method is constructed to demonstrate how non-parametrized SQL can lead to SQL injections
# FIX #2: Instead of this view use the view that used the built-in Django class SearchResultsView by modifying the urls.py
def search(request):
    query = request.GET.get('search_text')
    sql = "SELECT * FROM polls_question WHERE question_text LIKE '%" + query + "%'"
    search_results = Question.objects.raw(sql)
    return render(request, 'polls/search.html', {'object_list' : search_results})
