#-*- coding:utf-8 -*-
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

fix_link = "http://gall.dcinside.com"
upload_dir = '/home/vagrant/project/japan_service/collect/'

url = 'http://gall.dcinside.com/board/lists/?id=baseball_new6&page=1'
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

#while(True):
r = requests.get(url, headers=headers)

html = r.text

#rows = curs.fetchall()

soup = BeautifulSoup(html, "lxml")
link = soup.find_all("td", { "class" : "t_subject" })

ccc = 0
for m in link:
    if(m.find("a", {"class":"icon_pic_n"})) and ccc == 0:
        post_number = m.parent.find("td", {"class" : "t_notice"}).string
        post_title = m.a.string
        print("post_number = ", post_number)
        #print("post_title = ", post_title)

        inner_link = fix_link + m.a.get('href') + "\n"
        #print(inner_link)
        r = requests.get(inner_link, headers=headers)

        #time.sleep(5)

        inner_html = r.text
        soup = BeautifulSoup(inner_html, "lxml")
        link2 = soup.find_all("li", { "class" : "icon_pic" })
        cnt = 0
        lock = 0
        for n in link2:
            if lock == 0:
                pure_file_name = n.a.string
                file_link = n.a.get('href')
                #print("pure_file_name = " + pure_file_name.encode('utf-8'))
                tmp_a = "http://image.dcinside.com/download.php"
                tmp_b = "http://dcimg2.dcinside.co.kr/viewimage.php"
                file_link = file_link.replace(tmp_a, tmp_b);
                #print("file_link = " + file_link)
                print("------------------------------------------------------------->")
                r = requests.get(file_link, headers=headers)
                fff = r.text
                img_file = urllib.request.urlopen(file_link)
                full_dir = upload_dir + post_number + '_' + str(cnt) + ".png"
                full_path = post_number + '_' + str(cnt) + ".png"
                try:
                    print(full_path)
                    curs = conn.cursor()
                    sql = '''
                        select count(id)
                        from picture
                        where file_name = '{filename}'
                    '''.format(filename=full_path)
                    curs.execute(sql)
                    rows = curs.fetchall()
                    print(rows[0][0])
                    if rows[0][0] == 0:
                        f = open(full_dir, 'wb')
                        #f.write(fff.read())
                        f.write(img_file.read())
                        f.close()
                        curs = conn.cursor()
                        sql = '''
                            insert into picture(file_name, file_dir,regist_date)
                            values('{filename}','{upload_dir}', now())
                        '''.format(filename=full_path, upload_dir=upload_dir)
                        curs.execute(sql)
                        conn.commit()
                        conn.close()
                except BaseException:
                    print("error!!!")
                cnt += 1
                lock += 1
                ccc += 1
