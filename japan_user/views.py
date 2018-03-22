#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connections
import hashlib, uuid
import urllib.parse
import requests
import json
from bs4 import BeautifulSoup

def boan_news(request, page_id, page, orderby):
    link_list = []
    subject_list = []
    link_list_real = []
    subject_list_real = []

    search_data = page_id
    search_data = search_data.encode('euc-kr')
    search_data = urllib.parse.quote(search_data)

    page = int(page)

    print("----------------->")
    print("page = ", page)
    print("orderby = ", orderby)
    print("----------------->")

    for p in range(1,page+1):
        url = 'http://www.boannews.com/search/news_list.asp?Page='+ str(p) +'&search=media&find=' + search_data
        print(url)

        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        subject_list = []
        link_list = []

        for link in soup.find_all("a"):
            if link.get('href').find('/media/view.asp') != -1:
                subject_list.append((link.text).encode('utf-8'))
                link_list.append(link.get('href').encode('utf-8'))

        for i in range(0, 40):
            if i % 2 == 0:
                subject_list_real.append(subject_list[i].strip().decode('unicode_escape').encode('iso8859-1').decode('utf-8'))
                link_list_real.append(link_list[i].strip().decode('unicode_escape').encode('iso8859-1').decode('utf-8'))

  
    print("---------------> len") 
    print("subject_list_real = ", len(subject_list_real)) 
    print("link_list_real = ", len(link_list_real)) 
    print("---------------> len")

    if orderby == 'true':
        subject_list_real.reverse()
        link_list_real.reverse()

    context = {}
    context['subject_list_real'] = subject_list_real
    context['link_list_real'] = link_list_real
    context['cnt'] = len(link_list_real)
    return render(request, 'japan_user/boannews.html', context)

def boannews(request):
    context = {}
    context['engine'] = 'mako'
    return render(request, 'japan_user/boannews.html', context)

def index(request):
    context = {}
    context['engine'] = 'mako'
    return render(request, 'japan_user/index.html', context)

def test(request):
    context = {}
    context['engine'] = 'mako'
    return render(request, 'japan_user/test.html', context)

def movie(request, page_id=None):

    print("page_id --------------->")
    print(page_id)
    print("page_id --------------->")

    if page_id == '1':
        movie = 'a.mp4'
        subject = '君の膵臓を食べたい'
    elif page_id == '2':
        movie = 'b.mp4'
        subject = 'ビリギャル'
    elif page_id == '3':
        movie = 'c.mp4'
        subject = 'オオカミ少女と黒王子'
    elif page_id == '4':
        movie = 'd.mp4'
        subject = 'デスノート'
    elif page_id == '5':
        movie = 'e.mp4'
        subject = 'オレンジ'
    elif page_id == '6':
        movie = 'f.mp4'
        subject = '今日昨日のきみとデートする'
    elif page_id == '7':
        movie = 'renai.mp4'
        subject = '恋愛ジンクス'
    elif page_id == '8':
        movie = 'g.mp4'
        subject = '君と100回目の恋'
    elif page_id == '9':
        movie = 'h.mp4'
        subject = 'airi no eiga'

    print("movie --------------->")
    print(movie)
    print("movie --------------->")

    context = {}
    context['movie'] = movie
    context['subject'] = subject
    return render(request, 'japan_user/movie.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def main(request, page_id=None):

    if request.is_ajax():
        print("ajax------------------")
        with connections['default'].cursor() as cur:
            query = '''
                select count(id) as cnt
                FROM japan_hanja
                where use_yn = 'y'
            '''
            cur.execute(query)
            rows = dictfetchall(cur)
            cnt = rows[0]['cnt']
        print(query)
        print(cnt)
        print("ajax------------------")
        #cur.close()
        return JsonResponse({'return':cnt})

    print("-------------------------------> id")
    print(page_id)
    print("-------------------------------> id")

    with connections['default'].cursor() as cur:
        query = '''
            select id, main, mean, um, hun
            FROM japan_hanja
            where seq = {page_id}
            and use_yn = 'y'
        '''.format(page_id=page_id)
        cur.execute(query)
        rows1 = dictfetchall(cur)

        print("-------------------> DEBUG")
        print(type(rows1))
        print(len(rows1))
        print("-------------------> DEBUG")

        if len(rows1) == 0:
            return HttpResponse("불법적인 접근입니다.<br> 정상적인 로직으로 접근하세요")

    with connections['default'].cursor() as cur:
        query = '''
            select word, hira, hangul
            from japan_um_word
            where hanja_id = {page_id}
        '''.format(page_id=page_id)
        cur.execute(query)
        rows2 = dictfetchall(cur)

    with connections['default'].cursor() as cur:
        query = '''
            select word, hira, hangul
            from japan_hun_word
            where hanja_id = {page_id}
        '''.format(page_id=page_id)
        cur.execute(query)
        rows3 = dictfetchall(cur)

    with connections['default'].cursor() as cur:
        query = '''
            select exam, hira, hangul
            from japan_exam
            where hanja_id = {page_id}
        '''.format(page_id=page_id)
        cur.execute(query)
        rows4 = dictfetchall(cur)

    #for row in rows:
    #    print(str(row).encode('utf-8'))

    rows1 = list(rows1)
    rows2 = list(rows2)
    rows3 = list(rows3)
    rows4 = list(rows4)

    context = {
        'rows1':rows1,
        'rows2': rows2,
        'rows3': rows3,
        'rows4': rows4,
        'page_id': page_id
    }
    context['engine'] = 'mako'
    return render(request, 'japan_user/main.html', context)

@csrf_protect
def regist(request):

    print("=======================> 1")

    email = request.POST.get('email')
    password = request.POST.get('password')
    password_check = request.POST.get('password_check')
    username = request.POST.get('username')
    level = request.POST.get('level')
    mode = request.POST.get('mode')

    salt = 'hellojapan123!@#'
    hashed_password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

    if email == '':
        return JsonResponse({'return': '1'})
    elif password == '':
        return JsonResponse({'return': '2'})
    elif username == '':
        return JsonResponse({'return': '3'})
    elif level == 'none':
        return JsonResponse({'return': '4'})
    elif mode != 'regist':
        return JsonResponse({'return': '5'})
    elif password_check == '':
        return JsonResponse({'return': '6'})

    #DEBUG
    print("email = ", email)
    print("password = ", password)
    print("password_check = ", password_check)
    print("username = ", email)
    print("level = ", level)
    print("mode = ", mode)

    with connections['default'].cursor() as cur:
        query = """
            select count(email)
            from japan_user
            where email = '{email}'
        """.format(email=email)
        cur.execute(query)
        rows = cur.fetchall()

    if rows[0][0] != 0:
        return JsonResponse({'return': '99'})

    if password != password_check:
        return JsonResponse({'return': '50'})

    with connections['default'].cursor() as cur:
        query = """
            insert into japan_user(email, password, username, level)
            values('{email}', '{password}', '{username}', '{level}')
        """.format(email=email, password=hashed_password, username=username, level=level)
        cur.execute(query)

    context = {}
    return JsonResponse({'return':'0'})

@csrf_protect
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    mode = request.POST.get('mode')

    #DEBUG
    print("email = ", email)
    print("password = ", password)
    print("mode = ", mode)

    salt = 'hellojapan123!@#'
    hashed_password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()


    if email == '':
        return JsonResponse({'return': '1'})
    elif password == '':
        return JsonResponse({'return': '2'})
    elif mode != 'login':
        return JsonResponse({'return': '3'})

    with connections['default'].cursor() as cur:
        query = """
            select email, is_staff
            from japan_user
            where email = '{email}' and password = '{password}'
        """.format(email=email, password=hashed_password)

        print(query)

        cur.execute(query)
        rows = dictfetchall(cur)

    print("---------------->",len(rows))

    if len(rows) == 0:
        return JsonResponse({'return': '5'})

    print("----------------> rows")
    print(rows)
    print("----------------> rows")
    if rows[0]['is_staff'] == 1:
        return JsonResponse({'return':'999'})

    return JsonResponse({'return':'0'})
