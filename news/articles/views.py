from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy

# Create your views here.

from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(ListView):
    model = Article
    template_name = 'article_detail.html'

class ArticleUpdateView(ListView):
    model = Article
    fields = ['title', 'body', ]
    template_name = 'article_edit.html'

class ArticleDeleteView(ListView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')