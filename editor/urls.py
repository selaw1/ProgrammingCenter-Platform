from django.urls import path

from . import views


app_name = 'editor'

urlpatterns = [
    path('', views.home , name='home'),
    path('compiler/', views.compiler, name='compiler'),
    path('compiler/web/', views.web_compiler, name='web_compiler'),
    path('compiler/run/', views.run_code , name='run'),
]
