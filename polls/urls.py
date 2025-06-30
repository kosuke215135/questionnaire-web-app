from django.urls import path
from . import views

__all__ = ['DetailView', 'ResultsView', 'vote']

urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
] 