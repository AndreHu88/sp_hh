from pyquery import PyQuery as pq

doc = pq('http://maoyan.com/films')
print(type(doc))
print(doc('a[href='))