from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/add/', views.add, name='add'),
    # FLAW #2: SQL Injection. The custom search-view has broken funtionality enabling SQL injections.
    #
    # TESTING: The user given search terms are processed unsatinized as raw SQL. This flaw is the same as Securing Software task
    # Part3-14.injection. You can use the following as a search string (asdf' union select password from Users where admin like '%1)
    # If DEBUG = True in settings.py, it shows that it tries to process the search term as an unsanitized SQL statement, but ends in an error because
    # no table Users exists. If the debug mode is disabled, the server reports 500 error which can indicate to the attacker that the program is
    # subject to an SQL injection
    #
    # FIX #2: Instead of the search-view, use the view below that uses built-in Django SearchResultView by commenting line 19 and uncommenting line 20
    path('search/', views.search, name='search')
    # path('search/', views.SearchResultsView.as_view(), name='search')
]