from django.urls import path

from .views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name = 'article_list'),
    path('<int:pk>/edit/', ArticleListView.as_view(), name = 'article_edit'),
    path('<int:pk>/', ArticleListView.as_view(), name = 'article_detail'),
    path('<int:pk>/delete/', ArticleListView.as_view(), name = 'article_delete'),
]