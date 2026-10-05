import urllib.request,urllib.error,json,subprocess,time

def get(url):
 with urllib.request.urlopen(url,timeout=10) as r: return r.read(),r.headers
body,headers=get('http://localhost:8080/health/')
assert json.loads(body)['database']=='connected'
for h in ['X-Content-Type-Options','X-Frame-Options','Content-Security-Policy']: assert headers.get(h),h
print('PASS: web, DB health, proxy headers')
for i in range(24):
 try:
  targets=json.loads(get('http://localhost:9090/api/v1/targets')[0])['data']['activeTargets']
  if len(targets)==5 and all(t['health']=='up' for t in targets): break
 except Exception: pass
 time.sleep(5)
else: raise SystemExit('FAIL: Prometheus targets are not all UP')
for query in ['pg_up','nginx_up']:
 data=json.loads(get('http://localhost:9090/api/v1/query?query='+query)[0])['data']['result']
 assert data and all(x['value'][1]=='1' for x in data),query
print('PASS: 5 targets UP, pg_up=1, nginx_up=1')
try: get('http://localhost:8080/demo-not-found')
except urllib.error.HTTPError as e: assert e.code==404
get('http://localhost:3000/api/health'); print('PASS: Grafana health')
# Internal Loki read through existing Grafana container, no host port exposed.
for i in range(12):
 r=subprocess.run(['docker','compose','exec','-T','grafana','wget','-qO-','http://loki:3100/loki/api/v1/label/job/values'],capture_output=True,text=True)
 if r.returncode==0 and 'nginx' in json.loads(r.stdout).get('data',[]): break
 time.sleep(5)
else: raise SystemExit('FAIL: no nginx stream in Loki; inspect promtail/loki logs')
print('PASS: nginx log stream ingested into Loki')
print('Still verify dashboard charts, 3 LogQL queries and pgAdmin visually; see docs/DEMO_CHECKLIST.md')
