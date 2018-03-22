from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [

    # django 어드민 페이지
    path('django_admin', admin.site.urls),

    # 어드민 사이트
    path('admin', include('japan_admin.urls')),

    # 사용자 사이트
    url(r'^', include('japan_user.urls')),


]
