import urllib.parse
 
url = "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=49513"
result = urllib.parse.urlsplit(url)
query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
ip = urllib.parse.urlsplit(url).netloc
 
path = urllib.parse.urlsplit(url).path
new_url = urllib.parse.urlparse(url)
 
 
print('第一、urllib.parse.urlsplit(url)=', result)
print('第二、dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))=', query)
print('ip或者域名=', ip)
print('ip或者域名=', new_url.netloc)
print('path路径=', path)
print('id=', query['id'])
