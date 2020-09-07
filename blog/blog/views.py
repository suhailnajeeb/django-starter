from django.views.generic import ListView
from django.shortcuts import render
from .models import Post

# Create your views here.

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'