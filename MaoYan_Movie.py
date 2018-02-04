# coding=utf-8

# 多线程使用
# name = multiprocessing.current_process().name 获取当前进程的名字
# process_1 = multiprocessing.Process(name='001', target=main()) 在进程中调用main方法
# process_1.start()  开启线程
# 打印出所有的线程    print(threading.enumerate())

import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool
import pymysql

db_connection = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                db='spider',
                charset='utf8'
            )

proxies_ip = '190.11.24.66:53281'


# 获取猫眼电影的数据
def get_movie_index(request_type, offset):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    request_headers = {'User-Agent': user_agent}
    proxies = {"http": proxies_ip}
    url = 'http://maoyan.com/films?showType={0}&offset={1}'.format(request_type, offset)
    # url = 'http://ip.chinaz.com'
    print('开始获取%s' % url)
    try:
        response = requests.get(url, headers=request_headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        else:
            return None
    except RequestException:
        return None


def get_all_movie_id(html):
    pattern = 'movieid:(.*?)}'
    result = re.findall(re.compile(pattern, re.S), html)
    if result:
        return result
    else:
        print(html)
        print("没有匹配到结果")
        return None


# 获取每个电影的详情页数据
def get_movie_detail_html(movie_id):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    request_headers = {'User-Agent': user_agent}
    proxies = {"http": proxies_ip}
    url = 'http://maoyan.com/films/' + movie_id
    print(url)
    try:
        response = requests.get(url, headers=request_headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            detail_html = response.text
            # 获取每个页面的数据
            return detail_html
        else:
            print("解析URL错误") + url
            return None
    except RequestException as e:
        print(format(e))
        return None


# 匹配电影的简介信息
def get_movie_intro(html):
    # 匹配图片 名字 英文名字 剧情介绍
    pattern = '<img class="avatar" src="(.*?)"' \
              '.*?<h3 class="name">(.*?)</h3>' \
              '.*?<div class="ename ellipsis">(.*?)</div>' \
              '.*?</li>.*?<span class="dra">(.*?)</span>'
    result = re.findall(re.compile(pattern, re.S), html)
    dict = {}
    if result:
        item = result[0]
        dict['image'] = item[0]
        dict['name'] = item[1]
        dict['english_name'] = item[2]
        dict['intro'] = item[3]

    # 获取时长 类型 上映时间
    info_pattern = '<li class="ellipsis">(.*?)</li>'
    info_result = re.findall(re.compile(info_pattern, re.S), html)
    if info_result:
        area_list = info_result[1].lstrip('\n ').split('/')
        dict['type'] = info_result[0]
        dict['area'] = area_list[0].rstrip()
        dict['duration'] = area_list[1].rstrip() if len(area_list) > 1 else '暂无时长'
        dict['show_time'] = info_result[2]
    return dict


# 匹配演员信息
def get_actor_info(html):
    # 匹配导演 主演 编剧
    # <li class="celebrity ".*?class="name">\n      (.*?)\n    </a>
    director_pattern = '<li class="celebrity " data.*?target="_blank" class="name">\n      (.*?)\n    </a>'
    director_result = re.findall(re.compile(director_pattern, re.S), html)
    director = ''
    if director_result:
        director = director_result[0]
    # print('导演:' + director)

    actor_pattern = '<li class="celebrity actor".*?target="_blank" class="name">\n      (.*?)\n    </a>'
    actor_result = re.findall(re.compile(actor_pattern, re.S), html)
    actor_str = ''
    if actor_result:
        actor_str = ','.join(actor_result)
    # print('演员：' + actor_str)
    return [director, actor_str]


# 获取每个页面的匹配结果
def get_movie_detail_info(html):
    info_result = get_movie_intro(html)
    actor_info = get_actor_info(html)
    info_result['director'] = actor_info[0]
    info_result['actor'] = actor_info[1]
    return info_result


def save_to_db(result):
    insert_sql = "insert into %s (name,english_name,image,intro,movie_type,show_area,show_time,director," \
                 "actor,duration) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                 % ('movie', result['name'], result['english_name'], result['image'], result['intro'],
                    result['type'], result['area'], result['show_time'], result['director'], result['actor'],
                    result['duration'])
    print(insert_sql)
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(insert_sql)
            db_connection.commit()
    except pymysql.MySQLError as e:
        print('插入数据库失败了',e)
    finally:
        db_connection.rollback()


def main(offset):
    html = get_movie_index(1, offset)
    if html:
        movie_id_list = get_all_movie_id(html)
        for movie_id in movie_id_list:
            movie_detail_html = get_movie_detail_html(movie_id)
            if movie_detail_html:
                movie_info_dict = get_movie_detail_info(movie_detail_html)
                if movie_info_dict:
                    save_to_db(movie_info_dict)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 30 for i in range(0, 300)])