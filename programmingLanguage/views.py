from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from .models import Category, Language, DataStructure


def home(request):
    return render(request, 'pl/home.html')


class CategoryListView(ListView):
    model = Category
    template_name = 'pl/category.html'
    context_object_name = 'categories'


def category_detail(request, path, instance):

    web = Category.objects.get(name='Web')
    mobile = Category.objects.get(name='Mobile')
    games = Category.objects.get(name='Games')
    data = Category.objects.get(name='Data Science')
    
    return render(
        request,
        'pl/category_detail.html',
        {
            'web':web,
            'mobile':mobile,
            'games':games,
            'data':data,
            'instance': instance,
            'languages': Language.objects.filter(category=instance),
            'children': instance.get_children() if instance else Category.objects.root_nodes(),
        }
    )


# Context Manager for all pages to access
def language_list(request):
    language_list = Language.objects.all()
    context = {
        'language_list': language_list
    }
    return context


def language_page(request):
    return render(request, 'pl/languages.html')

class LanguagesDetailView(DetailView):
    model = Language
    template_name = 'pl/languages_detail.html'


class DataStructureDetailView(DetailView):
    model = DataStructure
    template_name = 'pl/datastructure_detail.html'


