from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.detail import DetailView as DjangoDetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView as GenericDetailView
from django.http import HttpResponse
from .models import Question, Choice
from django.urls import reverse

__all__ = ['DetailView', 'ResultsView', 'vote']

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
        # 結果ページへリダイレクト
        return redirect('polls:results', pk=question.pk)
