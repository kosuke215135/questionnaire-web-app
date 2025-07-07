from django.urls import path
from . import views
from .views import SurveyDetailView, SurveyResultsView, survey_vote

__all__ = ['DetailView', 'ResultsView', 'vote']

urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('survey/<int:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('survey/<int:pk>/results/', SurveyResultsView.as_view(), name='survey_results'),
    path('survey/<int:pk>/vote/', survey_vote, name='survey_vote'),
] 
