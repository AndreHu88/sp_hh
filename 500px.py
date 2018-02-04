
import requests
from requests.exceptions import RequestException
import re
from lxml import etree

def get_html_content():
    request_headers = {
        'Host':    'api.500px.com',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
        'Referer' : 'https://500px.com/lishaofu/galleries/fit',
        'Origin': 'https: // 500px.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
    }
    url = 'https://api.500px.com/v1/users/15228257/galleries/22728937/items?rpp=50&image_size%5B%5D=1&image_size%5B%5D=2&image_size%5B%5D=32&image_size%5B%5D=31&image_size%5B%5D=33&image_size%5B%5D=34&image_size%5B%5D=35&image_size%5B%5D=36&image_size%5B%5D=2048&image_size%5B%5D=4&image_size%5B%5D=14&include_licensing=true&formats=jpeg%2Clytro&sort=position&sort_direction=asc&page=1&rpp=50'
    print('开始获取%s' % url)
    cookies = dict(Cookie='optimizelyEndUserId=oeu1517711538767r0.3968800404295101; optimizelySegments=%7B%22569090246%22%3A%22false%22%2C%22569491641%22%3A%22direct%22%2C%22575800731%22%3A%22gc%22%2C%22589900200%22%3A%22true%22%7D; optimizelyBuckets=%7B%7D; _ga=GA1.2.1845369598.1517711539; _gid=GA1.2.738694285.1517711539; __gads=ID=cc94a252a23596b6:T=1517711539:S=ALNI_MYOGMFURWhmZ_d3puu_w7OjUwbTTg; device_uuid=a6b00a94-6579-4443-891d-c095e9bd8ced; __hstc=133410001.758a311c427ea9b3132d2822bc261bc2.1517711671350.1517711671350.1517711671350.1; __hssrc=1; hubspotutk=758a311c427ea9b3132d2822bc261bc2; amplitude_id500px.com=eyJkZXZpY2VJZCI6ImFkYTA2N2VlLWI4OWQtNDZkMi04OGU4LWZiYWQxMWQ1NjRjZlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTUxNzcxMzY4MzAzOSwibGFzdEV2ZW50VGltZSI6MTUxNzcxMzY4MzAzOSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; optimizelyPendingLogEvents=%5B%22n%3Doptly_activate%26u%3Doeu1517711538767r0.3968800404295101%26wxhr%3Dtrue%26time%3D1517713684.425%26f%3D10086591487%2C9502403088%2C8746762262%2C9737453591%2C9729990917%2C9502690399%2C8478672984%2C9661320798%2C9738180735%2C9503661200%2C9732794009%2C8179770025%2C8781643456%2C10168315076%2C10090402082%2C9510832862%2C9494972573%2C8478040821%2C8560956350%2C8484780344%2C9660800875%2C9518490284%2C10034978693%2C10053048254%2C8740624971%2C9510101479%26g%3D%22%2C%22n%3Dhttps%253A%252F%252F500px.com%252Flishaofu%252Fgalleries%252Ffit%26u%3Doeu1517711538767r0.3968800404295101%26wxhr%3Dtrue%26time%3D1517713684.396%26f%3D10086591487%2C9502403088%2C8746762262%2C9737453591%2C9729990917%2C9502690399%2C8478672984%2C9661320798%2C9738180735%2C9503661200%2C9732794009%2C8179770025%2C8781643456%2C10168315076%2C10090402082%2C9510832862%2C9494972573%2C8478040821%2C8560956350%2C8484780344%2C9660800875%2C9518490284%2C10034978693%2C10053048254%2C8740624971%2C9510101479%26g%3D582890389%22%5D; _hpx1=BAh7C0kiD3Nlc3Npb25faWQGOgZFVEkiJTdkMTJmOWNjNTQ0ZGZmNTRiNjhkY2RjNWMzMDQyMjM2BjsAVEkiCWhvc3QGOwBGIhJhcGkuNTAwcHguY29tSSIZdXNlX29uYm9hcmRpbmdfbW9kYWwGOwBGVEkiGHN1cGVyX3NlY3JldF9waXgzbHMGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMVdGeXlDMkdlTlc5WllYemIvbFZjbmZxRTY2WkNwZ1RMSHJyanFEK25hODA9BjsARkkiEXByZXZpb3VzX3VybAY7AEZJIhwvbGlzaGFvZnUvZ2FsbGVyaWVzL2ZpdAY7AFQ%3D--3c5b45e57a35429abef2ba032567b26180aa42ee')
    try:
        response = requests.get(url , headers = request_headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            print(html)
        else:
            print(response.text)
            return None
    except RequestException:
        print(RequestException)
        return None


def main():
    get_html_content()


if __name__ == '__main__':
    main()