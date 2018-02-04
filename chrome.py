from selenium import webdriver
from bs4 import BeautifulSoup
import time
from lxml import etree
import re

def get_image_re(html):
    pattern = 'class="photo_thumbnail.*?data-src.*?src="(.*?)\?webp'
    result = re.findall(re.compile(pattern, re.S), html)
    if result:
        for url in result:
            print(url)
        print(result)
    else:
        print(html)
        print("没有匹配到结果")
        return None


def main():
    browser = webdriver.Chrome()
    browser.get('https://500px.com/lishaofu/galleries/fit')
    print('ok')
    html = browser.page_source
    print(html)
    get_image_re(html)

if __name__ == '__main__':
    main()