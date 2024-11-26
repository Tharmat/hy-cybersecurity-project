from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # FLAW #2: SQL Injection. The custom search-view has broken funtionality enabling SQL injections.
    # FIX #2: Instead of the search-view, use the view below that uses built-in Django SearchResultView by uncommenting line 14 and commenting line 13
    path('search/', views.search, name='search')
    # path('search/', views.SearchResultsView.as_view(), name='search')
]