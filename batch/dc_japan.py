import requests
import urllib.request
import pymysql
from bs4 import BeautifulSoup
import time

conn = pymysql.connect(
    host='127.0.0.1',
    user='japan_service',
    password='0000',
    db='japan_service',
    charset='utf8'
)

def dc_data(gall_id):

    context = {}

    url = 'http://gall.dcinside.com/board/lists/?id=' + gall_id
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'gall.dcinside.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("tr",{ "class" : "tb" })

    for link in links:
        notice = link.find_all("td",{ "class" : "t_notice" })
        if notice[0].string.isdigit() == True:
            t_writer = link.find_all("td",{ "class" : "t_writer" })
            user_ip = link.find_all("span",{ "class" : "user_ip" })

            data_num = notice[0].string
            data_subject = link.a.string
            try:
                data_writer = t_writer[0]['user_name']
                data_ip = user_ip[0].string.replace('(','').replace(')','')
            except BaseException:
                data_writer = t_writer[0]['user_name']
                data_ip = "fix"

            inner_link = 'http://gall.dcinside.com/board/view/?id=japanese&no=' + data_num

            r = requests.get(inner_link, headers=headers)
            html = r.text
            soup = BeautifulSoup(html, "lxml")
            links = soup.find_all("div",{ "class" : "s_write" })

            for link in links:
                data_content = link.text

            context['data_num'] = data_num
            context['data_subject'] = data_subject
            context['data_writer'] = data_writer
            context['data_ip'] = data_ip
            context['inner_link'] = inner_link
            context['data_content'] = data_content.strip()

            return context

if __name__ == "__main__":

    context = dc_data('japanese')

    #print("data_num = ",context['data_num'])
    #print("data_subject = ",context['data_subject'])
    #print("data_writer = ",context['data_writer'])
    #print("data_ip = ",context['data_ip'])
    #print("inner_link = ",context['inner_link'])
    #print("data_content = ",context['data_content'])

    curs = conn.cursor()
    sql = '''
        select max(data_num)
        from dc_japanese
        order by regist_date desc
    '''
    curs.execute(sql)
    rows = curs.fetchall()

    if(int(context['data_num']) > int(rows[0][0])):
        curs2 = conn.cursor()
        sql2 = '''
            insert into dc_japanese(data_num, data_subject, data_content, data_writer, data_ip)
            values('{data_num}', '{data_subject}', '{data_content}', '{data_writer}', '{data_ip}')
        '''.format(
            data_num = str(context['data_num']),
            data_subject = str(context['data_subject']),
            data_content = str(context['data_content']),
            data_writer = str(context['data_writer']),
            data_ip = str(context['data_ip']),
        )
        curs2.execute(sql2)
        conn.commit()
        conn.close()
