from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connections

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def index(request):
    with connections['default'].cursor() as cur:
        query = '''
            SELECT seq, main, mean, um, hun, 
            CASE 
              when level = 'l1'
              THEN '소학교 1학년'
              when level = 'l2'
              THEN '소학교 2학년'
              when level = 'l3'
              THEN '소학교 3학년'
              when level = 'l4'
              THEN '소학교 4학년'
              when level = 'l5'
              THEN '소학교 5학년'
              when level = 'l6'
              THEN '소학교 6학년'
              when level = 'l7'
              THEN '중학교'
            end as level
            , regist_date
            FROM japan_hanja
            where use_yn = 'y'
            ORDER BY id DESC
        '''
        cur.execute(query)
        rows = dictfetchall(cur)

    context = {}
    context['rows'] = rows
    return render(request, 'japan_admin/index.html', context)

def user(request):
    with connections['default'].cursor() as cur:
        query = '''
            SELECT id, email, username, level,
            case
                when is_staff = 0
                then '일반'
                when is_staff = 1
                then '관리자'
            end is_staff
                , regist_date
            FROM japan_user
        '''
        cur.execute(query)
        rows = dictfetchall(cur)

    context = {}
    context['rows'] = rows
    return render(request, 'japan_admin/user.html', context)

def hanja_regist(request):

    with connections['default'].cursor() as cur:
        query = '''
            select max(seq) as seq
            FROM japan_hanja
        '''
        cur.execute(query)
        check = dictfetchall(cur)
    seq = check[0]['seq']

    context = {}
    context['seq'] = seq
    return render(request, 'japan_admin/hanja_regist.html', context)

def hanja_regist_view(request):
    seq = request.POST.get('seq')
    main = request.POST.get('main').encode('utf-8')
    mean = request.POST.get('mean').encode('utf-8')
    level = request.POST.get('level').encode('utf-8')
    um = request.POST.get('um').encode('utf-8')
    hun = request.POST.get('hun').encode('utf-8')
    um_word = request.POST.get('um_word')
    hun_word = request.POST.get('hun_word')
    exam_word = request.POST.get('exam_word')

    print("---------------------------------> s")
    #print("main = ", main)
    #print("mean = ", mean)
    #print("level = ", level)
    #print("um = ", um)
    #print("hun = ", hun)
    #print("um_word = ", um_word)
    #print("hun_word = ", hun_word)
    #print("exam_word = ", exam_word)
    print("---------------------------------> e")

    if len(um) == 0:
        um = 'none'.encode('utf-8')
    if len(hun) == 0:
        hun = 'none'.encode('utf-8')

    with connections['default'].cursor() as cur:
        query = '''
            select count(seq) as seq
            FROM japan_hanja
            where seq = {seq}
        '''.format(seq=seq)
        cur.execute(query)
        check = dictfetchall(cur)

    if check[0]['seq'] == 1 :
        return JsonResponse({'return':'duplication'})

    with connections['default'].cursor() as cur:
        query = '''
            insert into japan_hanja(seq, main, mean, um, hun, level)
            values('{seq}', '{main}', '{mean}', '{um}', '{hun}', '{level}')
        '''.format(
            seq=seq,
            main=main.decode('unicode_escape').encode('iso8859-1').decode('utf8'),
            mean=mean.decode('unicode_escape').encode('iso8859-1').decode('utf8'),
            um=um.decode('unicode_escape').encode('iso8859-1').decode('utf8'),
            hun=hun.decode('unicode_escape').encode('iso8859-1').decode('utf8'),
            level=level.decode('unicode_escape').encode('iso8859-1').decode('utf8')
        )
        cur.execute(query)

    with connections['default'].cursor() as cur:
        query = '''
            select max(seq) as last_id
            FROM japan_hanja
            order by regist_date desc
        '''
        cur.execute(query)
        rows = dictfetchall(cur)

    last_id = rows[0]['last_id']

    # 음독 단어 입력 --------------------------------------------------------------->
    um_word_list = um_word.split('/')
    um_word_list.pop()

    with connections['default'].cursor() as cur:
        for item in um_word_list:
            tmp = item.split('+')
            #print(tmp[0])
            #print(tmp[1])
            #print(tmp[2])
            query = '''
                 insert into japan_um_word(hanja_id, word, hira, hangul)
                 value({last_id}, '{word}', '{hira}', '{hangul}')
            '''.format(last_id=last_id, word=tmp[0],hira=tmp[1],hangul=tmp[2])
            #print(query)
            cur.execute(query)

    # 훈독 단어 입력 --------------------------------------------------------------->
    hun_word_list = hun_word.split('/')
    hun_word_list.pop()

    tmp = None
    with connections['default'].cursor() as cur:
        for item in hun_word_list:
            tmp = item.split('+')
            #print(tmp[0])
            #print(tmp[1])
            #print(tmp[2])
            query = '''
                 insert into japan_hun_word(hanja_id, word, hira, hangul)
                 value({last_id}, '{word}', '{hira}', '{hangul}')
            '''.format(last_id=last_id, word=tmp[0],hira=tmp[1],hangul=tmp[2])
            #print(query)
            cur.execute(query)

    # 예시 입력 --------------------------------------------------------------->
    exam_word_list = exam_word.split('/')
    exam_word_list.pop()

    tmp = None
    with connections['default'].cursor() as cur:
        for item in exam_word_list:
            tmp = item.split('+')
            #print(tmp[0])
            #print(tmp[1])
            #print(tmp[2])
            query = '''
                 insert into japan_exam(hanja_id, exam, hira, hangul)
                 value({last_id}, '{word}', '{hira}', '{hangul}')
            '''.format(last_id=last_id, word=tmp[0],hira=tmp[1],hangul=tmp[2])
            #print(query)
            cur.execute(query)

    return JsonResponse({'foo':'bar'})