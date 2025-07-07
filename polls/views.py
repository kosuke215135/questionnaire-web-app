from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.detail import DetailView as DjangoDetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView as GenericDetailView, ListView
from django.http import HttpResponse
from .models import Question, Choice, Survey
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

__all__ = ['DetailView', 'ResultsView', 'vote', 'SurveyDetailView', 'SurveyResultsView', 'survey_vote']

# Create your views here.

class DetailView(GenericDetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(GenericDetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, question.choice_set.model.DoesNotExist):
        # 選択肢が選ばれていない場合、エラーメッセージ付きで詳細ページを再表示
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': '選択肢を選んでください。',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # サーベイの集計結果ページへリダイレクト
        return redirect('polls:survey_results', pk=question.survey.pk)

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'polls/survey_detail.html'
    context_object_name = 'survey'

class SurveyResultsView(DetailView):
    model = Survey
    template_name = 'polls/survey_results.html'
    context_object_name = 'survey'

def survey_vote(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == 'POST':
        for question in survey.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                try:
                    selected_choice = Choice.objects.get(pk=choice_id, question=question)
                    selected_choice.votes += 1
                    selected_choice.save()
                except Choice.DoesNotExist:
                    pass  # 不正な選択肢IDは無視
        return redirect('polls:survey_results', pk=survey.pk)
    else:
        return redirect('polls:survey_detail', pk=survey.pk)
