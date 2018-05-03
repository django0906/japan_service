import pymysql
from collections import Counter
from konlpy.tag import Twitter
import pytagcloud

conn = pymysql.connect(
    host='127.0.0.1',
    user='japan_service',
    password='0000',
    db='japan_service',
    charset='utf8'
)

data_list = ''

curs = conn.cursor()
sql = '''
    select data_subject
    from dc_japanese
'''
sql2 = '''
    select data_content
    from dc_japanese
'''
sql3 = '''
    select data_writer
    from dc_japanese
'''
curs.execute(sql)
rows = curs.fetchall()

for row in rows:
    try:
        data_list += row[0]
    except BaseException:
        pass

nlp = Twitter()  
nouns = nlp.nouns(data_list)
count = Counter(nouns)
tag2 = count.most_common(30)
taglist = pytagcloud.make_tags(tag2, maxsize=80)
pytagcloud.create_tag_image(taglist, '/home/vagrant/project/japan_service/media/word/wordcloud.jpg', size=(700, 700), fontname='korean', rectangular=False)

