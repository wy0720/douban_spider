#coding:utf - 8
import requests
from urllib.parse import urlencode
import json
import time
from bs4 import BeautifulSoup

def single_page(offset):
    header = {
        "Cookie":"ll='108296'; bid=zRtenT25h5E; ap_v=0,6.0; __utma=30149280.1616863212.1538992574.1538992574.1538992574.1; __utmb=30149280.0.10.1538992574; __utmc=30149280; __utmz=30149280.1538992574.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1537191320.1538992574.1538992574.1538992574.1; __utmb=223695111.0.10.1538992574; __utmc=223695111; __utmz=223695111.1538992574.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_ses.100001.4cf6=*; __yadk_uid=Y0Az4p7TZ8R7pXoFWGR87paMTZLWmKa9; _vwo_uuid_v2=D49BBB9F67812B5A0128E38880BBEC8C7|139a1793db0ce6230e061517a0d788b2; _pk_id.100001.4cf6=7a3ffe9cfc9b2e4a.1538992574.1.1538994825.1538992574.",
        "Host": "movie.douban.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    param = {
        "type": "movie",
        "tag": "豆瓣高分",
        "sort": "recommend",
        "page_limit": 20,
        "page_start": offset
    }
    url = "https://movie.douban.com/j/search_subjects?" + urlencode(param)

    try:
        result = requests.get(url, header)
        return result
    except:
        return None

#详情页
def find_detail(url, obj):
    header = {
        'Cookie':'ll="108296"; bid=zRtenT25h5E; __utmc=30149280; __utmz=30149280.1538992574.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=223695111; __utmz=223695111.1538992574.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=Y0Az4p7TZ8R7pXoFWGR87paMTZLWmKa9; _vwo_uuid_v2=D49BBB9F67812B5A0128E38880BBEC8C7|139a1793db0ce6230e061517a0d788b2; ap_v=0,6.0; _pk_ses.100001.4cf6=*; __utma=30149280.1616863212.1538992574.1539010120.1539013506.5; __utmb=30149280.0.10.1539013506; __utma=223695111.1537191320.1538992574.1539010120.1539013506.5; __utmb=223695111.0.10.1539013506; _pk_id.100001.4cf6=7a3ffe9cfc9b2e4a.1538992574.5.1539013599.1539010120.',
        'Host':'movie.douban.com',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    try:
        result = requests.get(url, header)
        bsObj = BeautifulSoup(result.text, 'lxml')
        person = bsObj.find_all('span', 'attrs')
        detail_obj = bsObj.find('span', property='v:summary')
        detail = detail_obj.text.replace('\n', '').strip().replace(' ', '').replace('\u3000', '')

        director = ''
        script_writer = ''
        actor = ''

        #导演
        for child in person[0]:
            director += child.string

        #编剧
        for child in person[1]:
            script_writer += child.string

        #主演
        for child in person[2]:
            actor += child.string

        obj['director'] = director
        obj['script_writer'] = script_writer
        obj['actor'] = actor
        obj['detail'] = detail

    except:
        print('ERROR')

def write_to_file(content):
    try:
        for key in content:
            key.pop('cover_x')
            key.pop('cover_y')
            key.pop('playable')
            key.pop('cover')
            key.pop('is_new')
            key.pop('id')
            find_detail(key['url'], key)
            data = json.dumps(key, ensure_ascii=False)
            fp = open('movie.txt', 'a', encoding='utf-8')
            fp.write(data +'\n')
    except:
        print('ERROR')
        return None

def main():
    limit = 20
    times = 0
    while(True):
        result = single_page(limit*times).json()
        times = times + 1
        write_to_file(result['subjects'])
        print(times)
        print(result['subjects'])
        time.sleep(4)
        if len((result['subjects'])) != 20:
            print('END')
            break
if __name__ == '__main__':
    main()