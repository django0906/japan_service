from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # 테스트 페이지
    path('test', views.test, name='test'),

    # 로그인 화면
    path('', views.index, name='index'),

    # 회원가입 처리
    path('regist', views.regist, name='regist'),

    # 로그인 처리
    path('login', views.login, name='login'),

    # 영화 페이지
    #path('movie', views.movie, name='movie'),
    url('movie/(?P<page_id>[0-9]{1,4})$', views.movie, name='main'),

    # 메인 페이지
    url('main/(?P<page_id>[0-9]{1,4})$', views.main, name='main'),

    # 보안뉴스 크롤링
    path('boannews', views.boannews, name='boannews'),
    url('boan_news/(?P<page_id>[a-zA-Zㄱ-힣]{1,10})&(?P<page>[0-9]{1,2})&(?P<orderby>[a-zA-Z]{1,10})$', views.boan_news, name='main'),
]
