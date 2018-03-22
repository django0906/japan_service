import sys
import argparse
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
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

API_URL = 'https://kapi.kakao.com/v1/vision/adult/detect'
MYAPP_KEY = 'dba87d5aa93baf300d6e6c5207bb6486'
FILENAME = ''

def detect_adult(image_url):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        data = { 'image_url' : image_url}
        resp = requests.post(API_URL, headers=headers, data=data)
        resp.raise_for_status()
        result = resp.json()['result']
        if result['adult'] > result['normal'] and result['adult'] > result['soft']:
            #print("adult {}% 입니다.".format(result['adult']*100))
            print("adult {0}".format(result['adult']*100))
            curs = conn.cursor()
            sql = '''
                update picture
                set normal = '0', soft = '0', adult = '{score}'
                where file_name = '{filename}'
            '''.format(filename=FILENAME, score=result['adult']*100)
            curs.execute(sql)
            conn.commit()
        elif result['soft'] > result['normal'] and result['soft'] > result['adult']:
            #print("soft {}% 입니다.".format(result['soft']*100))
            print("soft {0}".format(result['soft']*100))
            curs = conn.cursor()
            sql = '''
                update picture
                set normal = '0', soft = '{score}', adult = '0'
                where file_name = '{filename}'
            '''.format(filename=FILENAME, score=result['soft']*100)
            curs.execute(sql)
            conn.commit()
        else :
            #print("normal {}% 입니다.".format(result['normal']*100))
            print("normal".format(result['normal']*100))
            curs = conn.cursor()
            sql = '''
                update picture
                set normal = '{score}', soft = '0', adult = '0'
                where file_name = '{filename}'
            '''.format(filename=FILENAME, score=result['normal']*100)
            curs.execute(sql)
            conn.commit()

    except Exception as e:
        curs = conn.cursor()
        sql = '''
            update picture
            set normal = 'error', soft = 'error', adult = 'error'
            where file_name = '{filename}'
        '''.format(filename=FILENAME)
        curs.execute(sql)
        conn.commit()
        print(str(e))
        sys.exit(0)

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Classify adult image.')
    #parser.add_argument('image_url', type=str, nargs='?', default="http://t1.daumcdn.net/alvolo/_vision/openapi/r2/images/10.jpg")
    #args = parser.parse_args()
    #detect_adult(args.image_url)
  
    while(True):
        try:
            curs = conn.cursor()
            sql = '''
                select file_name
                from picture
                where normal is null or soft is null or adult is null;
            '''
            curs.execute(sql)
            rows = curs.fetchall()
            print(len(rows))
        except BaseException:
            pass
        if len(rows) != 0:
            rows = list(rows)
            print(rows)

            for i in range(0, len(rows)):
                time.sleep(5)
                try:
                    url = "http://selectahn.iptime.org/collect/" + rows[i][0]
                    parser = argparse.ArgumentParser(description='Classify adult image.')
                    parser.add_argument('image_url', type=str, nargs='?', default=url)
                    args = parser.parse_args()
                    print(url)
                    FILENAME = rows[i][0]
                    detect_adult(args.image_url)
                    print("---------------------------------->")

                except BaseException:
                    print("error")
            conn.close()
        else:
            print("time sleep 60 sec")
            time.sleep(60)
