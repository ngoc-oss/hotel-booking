"""Create temporary demo user and submit two overlapping reservations over HTTP.
Run on host after docker compose up. Leaves one confirmed booking for inspection.
"""
import urllib.request,urllib.parse,http.cookiejar,re,uuid,concurrent.futures
from datetime import date,timedelta
base='http://localhost:8080'
jar=http.cookiejar.CookieJar(); client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
def token(url):
 html=client.open(base+url).read().decode()
 return re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"',html).group(1)
def post(op,url,data): return op.open(base+url,urllib.parse.urlencode(data).encode()).read().decode()
t=token('/signup/'); username='race_'+uuid.uuid4().hex[:10]; password=uuid.uuid4().hex+'!A9'
post(client,'/signup/',dict(csrfmiddlewaretoken=t,username=username,password1=password,password2=password))
html=client.open(base).read().decode(); room=re.search(r'/rooms/(\d+)/book/',html).group(1)
url=f'/rooms/{room}/book/'; t=token(url)
start=date.today()+timedelta(days=100+int(uuid.uuid4().hex[:3],16))
data=dict(csrfmiddlewaretoken=t,guest_name='Concurrency demo',phone='0900000000',check_in=str(start),check_out=str(start+timedelta(days=2)),guests=1)
cookie='; '.join(c.name+'='+c.value for c in jar)
def submit(_):
 req=urllib.request.Request(base+url,urllib.parse.urlencode(data).encode(),headers={'Cookie':cookie})
 return urllib.request.urlopen(req).read().decode()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: results=list(ex.map(submit,range(2)))
assert sum('Phòng đã có khách' in s for s in results)==1, 'Expected exactly one overlap rejection'
assert sum('Đã xác nhận' in s for s in results)==1, 'Expected exactly one confirmed booking'
print('PASS: one success + one rejection on live stack. User:',username)
