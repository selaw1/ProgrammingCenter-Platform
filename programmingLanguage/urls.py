from django.urls import path, re_path
import mptt_urls

from . import views

app_name = 'pl'

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    # Category Main Page / Detail Category Page
    path('category/', views.CategoryListView.as_view(), name='category'),
    re_path(r'^category/(?P<path>.*)', mptt_urls.view(model='programmingLanguage.models.Category', view='programmingLanguage.views.category_detail', slug_field='slug',trailing_slash=True), name='category_detail'),
    # Programming Language Pages
    path('programming_languages/', views.language_page, name='languages'),
    path('programming_languages/<slug:slug>/', views.LanguagesDetailView.as_view(), name='languages_detail'),
    path('data_structure/<slug:slug>/', views.DataStructureDetailView.as_view(), name='datastructure_detail')
]
