"""Authorized team-intro production. Private inputs and responses stay outside Git."""
import argparse
import json
from pathlib import Path
import urllib.request
import uuid
import hashlib
import seedance25 as api

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'private/team-intro'
OUT.mkdir(parents=True, exist_ok=True)

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2), encoding='utf-8')

def doc():
    url = 'https://docs.apimart.ai/en/api-reference/videos/seedance-2-5/generation.md'
    source = urllib.request.urlopen(url, timeout=30).read().decode()
    (OUT/'provider-doc.md').write_text(source, encoding='utf-8')
    print(source[source.index('<ParamField body="image_urls"'):source.index('## Billing')])

def upload_team():
    if (OUT/'asset-submission.json').exists():
        raise RuntimeError('Asset already submitted; poll instead.')
    path = OUT/'team-endframe-v01.jpg'
    data = path.read_bytes()
    if (OUT/'team-upload.json').exists():
        upload = json.loads((OUT/'team-upload.json').read_text())
    else:
        boundary = 'voxwave' + uuid.uuid4().hex
        body = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="team-endframe-v01.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + data + f'\r\n--{boundary}--\r\n'.encode())
        upload = api.request('/v1/uploads/images', body, 'multipart/form-data; boundary='+boundary)
        save('team-upload.json', upload)
    payload = {'model':'seedance-2.5','group':{'name':'VoxWave-team-intro-v01'},'asset_type':'Image',
               'assets':[{'url':upload['url'],'name':'team-endframe-v01'}]}
    save('asset-submission.json', {'state':'dispatching','sha256':hashlib.sha256(data).hexdigest()})
    result = api.request('/v1/seedance2/private-avatar/assets',json.dumps(payload).encode())
    save('asset-submission.json', result)
    print(json.dumps(result))

def asset_status():
    submitted = json.loads((OUT/'asset-submission.json').read_text())
    task = submitted.get('id') or submitted.get('data',{}).get('id')
    if not task: raise RuntimeError('Inspect asset submission format')
    result = api.request('/v1/tasks/'+task)
    save('asset-status.json',result)
    print(json.dumps(result))

def prompt(shot):
    source = (ROOT/'video/script/team-intro-v01.md').read_text(encoding='utf-8')
    return source.split(f'## Plano {shot.upper()} — prompt\n\n')[1].split('\n\n## ')[0].strip()

def submit_a():
    submit('a', {'model':'seedance-2.5','resolution':'720p','size':'16:9','duration':5,
                 'generate_audio':False,'output_format':'mp4','return_last_frame':True,
                 'seed':11102601,'prompt':prompt('a')})

def submit(shot, payload):
    marker = OUT/f'{shot}-submission.json'
    if marker.exists(): raise RuntimeError('Already dispatched; do not resubmit.')
    save(f'{shot}-request.json',payload)
    save(f'{shot}-submission.json',{'state':'dispatching'})
    result = api.request('/v1/videos/generations',json.dumps(payload).encode())
    save(f'{shot}-submission.json',result)
    print(json.dumps(result))

def poll(shot):
    submitted = json.loads((OUT/f'{shot}-submission.json').read_text())
    task = submitted['data'][0]['task_id']
    result = api.request('/v1/tasks/'+task)
    save(f'{shot}-status.json',result)
    d = result['data']
    print(json.dumps({k:d.get(k) for k in ('status','progress','cost','estimated_time','error')}))

def poll_a(): poll('a')
def poll_b(): poll('b')

def download(shot):
    d=json.loads((OUT/f'{shot}-status.json').read_text())['data']
    assert d['status']=='completed'
    target = OUT/f'{shot}-v01.mp4'
    if target.exists(): raise RuntimeError('Already downloaded')
    with urllib.request.urlopen(d['result']['videos'][0]['url'][0],timeout=90) as src, target.open('xb') as dst:
        while block:=src.read(1024*1024): dst.write(block)
    print(str(target))

def download_a(): download('a')
def download_b(): download('b')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['doc','upload_team','asset_status','submit_a','poll_a','poll_b','download_a','download_b'])
    a = p.parse_args()
    globals()[a.action]()

if __name__ == '__main__':
    main()
