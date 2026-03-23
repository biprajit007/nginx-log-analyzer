from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import re
from collections import Counter

app = FastAPI(title='Nginx Log Analyzer')
LOG_RE = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>[^ ]+) (?P<proto>[^"]+)" (?P<status>\d{3}) \S+ "(?P<ref>[^"]*)" "(?P<ua>[^"]*)"')

@app.get('/', response_class=HTMLResponse)
def home():
    return """<html><body style='font-family:Arial;padding:20px'><h1>Nginx Log Analyzer</h1><form id='f'><input type='file' name='file'><button>Upload</button></form><pre id='out'></pre><script>
    f.onsubmit=async(e)=>{e.preventDefault();const fd=new FormData(f);const r=await fetch('/analyze',{method:'POST',body:fd});out.textContent=JSON.stringify(await r.json(),null,2)}
    </script></body></html>"""

@app.post('/analyze')
async def analyze(file: UploadFile = File(...)):
    text = (await file.read()).decode('utf-8', errors='ignore')
    ref_counter, path_counter, status_counter, ua_counter = Counter(), Counter(), Counter(), Counter()
    total = 0
    for line in text.splitlines():
        m = LOG_RE.match(line)
        if not m:
            continue
        total += 1
        ref_counter[m.group('ref')] += 1
        path_counter[m.group('path')] += 1
        status_counter[m.group('status')] += 1
        ua_counter[m.group('ua')] += 1
    return {
        'total_parsed': total,
        'top_referrers': ref_counter.most_common(10),
        'top_paths': path_counter.most_common(10),
        'status_codes': status_counter.most_common(),
        'top_user_agents': ua_counter.most_common(10),
    }
