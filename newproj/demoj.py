import urllib.request
f = open('00000001.jpg','wb')
f.write(urllib.request.urlopen('http://www.gunnerkrigg.com//comics/00000001.jpg').read())
f.close()