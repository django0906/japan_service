from django.urls import path
from . import views

urlpatterns = [
    path('/', views.index, name='index'),
    path('/hanja_regist', views.hanja_regist, name='hanja_regist'),
    path('/hanja_regist_view', views.hanja_regist_view, name='hanja_regist_view'),
    path('/user', views.user, name='user'),
]

