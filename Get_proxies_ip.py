# coding=utf-8
import requests
from requests.exceptions import RequestException
import re
from lxml import etree
from multiprocessing import Pool
import pymysql


# 获取西刺代理IP
def get_xc_index(page_no):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    request_headers = {'User-Agent': user_agent}
    url = 'http://www.xicidaili.com/wt/%s' % page_no
    print('开始获取%s' % url)
    try:
        response = requests.get(url, headers=request_headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            html_text = etree.HTML(html)
            result = html_text.xpath('//tr[@class="odd"]/td[2]/text()')
            print(result)
        else:
            return None
    except RequestException:
        return None


# 获取快代理IP
def get_kdl_index(page_no):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    request_headers = {'User-Agent': user_agent}
    url = 'http://www.kuaidaili.com/free/inha/%s' % page_no
    print('开始获取%s' % url)
    try:
        response = requests.get(url, headers=request_headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            html_text = etree.HTML(html)
            ip_address = html_text.xpath('//tr/td[1]/text()')
            port = html_text.xpath('//tr/td[2]/text()')
            for i in range(0, len(ip_address)):
                proxies_ip = '%s:%s' %(ip_address[i], port[i])
                i += 1
                print(proxies_ip)
        else:
            return None
    except RequestException:
        return None


def main():
    for i in range(1, 3000):
        get_kdl_index(i)
        i += 1


if __name__ == '__main__':
    main()