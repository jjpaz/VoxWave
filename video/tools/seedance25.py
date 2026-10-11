"""APIMart Seedance 2.5 workflow for the four reviewed synthetic shot references.

Explicit submit/poll/download commands, no automatic POST retries. Credentials
are read only from APIMART_API_KEY; requests never follow authentication redirects.
Provider responses, temporary URLs and generated media stay under ignored renders.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.request
import urllib.error
from urllib.parse import urlparse
import uuid

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'renders/seedance25'
CONFIG=json.loads((ROOT/'script/seedance25-shots-v01.json').read_text())
API='https://api.apimart.ai'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        return None


def save(path,data):
    path.write_text(json.dumps(data,indent=2),encoding='utf-8')


def request(path,body=None,content_type='application/json'):
    key=os.environ.get('APIMART_API_KEY')
    if not key: raise RuntimeError('APIMART_API_KEY is missing')
    req=urllib.request.Request(API+path,data=body,headers={
        'Authorization':'Bearer '+key,'Content-Type':content_type})
    try:
        with urllib.request.build_opener(NoRedirect).open(req,timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as error:
        raw=error.read().decode('utf-8',errors='replace').replace(key,'[REDACTED]')
        try: detail=json.loads(raw).get('error',{})
        except ValueError: detail={}
        message=detail.get('message','Provider HTTP error') if isinstance(detail,dict) else str(detail)
        raise RuntimeError(f'HTTP {error.code}: {message[:900]}') from None
    except urllib.error.URLError:
        raise RuntimeError('Network error; POST outcome may be unknown. Do not retry blindly.') from None


def submit(shot):
    folder=OUT/shot['id'];folder.mkdir(parents=True,exist_ok=True)
    if (folder/'dispatch.json').exists():
        raise RuntimeError('Dispatch already recorded. Inspect status; do not resubmit.')
    path=ROOT/'renders/keyframes'/shot['image']
    data=path.read_bytes()
    upload_path=folder/'upload.json'
    if upload_path.exists(): upload=json.loads(upload_path.read_text())
    else:
        boundary='voxwave'+uuid.uuid4().hex
        body=(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{shot["image"]}"\r\nContent-Type: image/png\r\n\r\n'.encode()
              +data+f'\r\n--{boundary}--\r\n'.encode())
        upload=request('/v1/uploads/images',body,'multipart/form-data; boundary='+boundary)
        save(upload_path,upload)
    assert urlparse(upload['url']).scheme=='https'
    payload={'model':CONFIG['model'],'resolution':CONFIG['resolution'],
        'size':'adaptive','duration':shot['duration'],'generate_audio':True,
        'output_format':'mp4','seed':10102500+int(shot['id'][1:]),
        'prompt':shot['prompt'],'image_with_roles':[{'url':upload['url'],'role':'first_frame'}]}
    save(folder/'request.json',payload)
    save(folder/'dispatch.json',{'state':'dispatching','image_sha256':hashlib.sha256(data).hexdigest()})
    result=request('/v1/videos/generations',json.dumps(payload).encode())
    save(folder/'submission.json',result)
    task=result['data'][0]['task_id']
    save(folder/'dispatch.json',{'state':'submitted','task_id':task,
        'image_sha256':hashlib.sha256(data).hexdigest()})
    print(json.dumps({'shot':shot['id'],'task_id':task,'status':'submitted'}),flush=True)


def poll(shot):
    folder=OUT/shot['id']
    state=json.loads((folder/'dispatch.json').read_text())
    result=request('/v1/tasks/'+state['task_id']+'?language=en')
    save(folder/'status.json',result)
    data=result['data']
    print(json.dumps({'shot':shot['id'],**{k:data.get(k) for k in
        ('status','progress','cost','estimated_time','actual_time','error')}}),flush=True)


def download(shot):
    folder=OUT/shot['id'];result=json.loads((folder/'status.json').read_text())['data']
    assert result['status']=='completed'
    url=result['result']['videos'][0]['url'][0]
    assert urlparse(url).scheme=='https'
    target=folder/(shot['id']+'-seedance25-'+CONFIG.get('version','v01')+'.mp4')
    if target.exists(): raise RuntimeError('Video already saved; not overwriting')
    # No credential header is sent to media/CDN hosts.
    with urllib.request.urlopen(url,timeout=180) as source,target.open('xb') as output:
        while block:=source.read(1024*1024):output.write(block)
    print(json.dumps({'shot':shot['id'],'saved':str(target),'bytes':target.stat().st_size}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['submit','poll','download'])
    p.add_argument('--config',default='seedance25-shots-v01.json',help='Config filename inside video/script')
    p.add_argument('shots',nargs='+',choices=[s['id'] for s in CONFIG['shots']])
    args=p.parse_args()
    config_path=(ROOT/'script'/args.config).resolve()
    if config_path.parent != (ROOT/'script').resolve():
        p.error('Config must be directly inside video/script')
    CONFIG=json.loads(config_path.read_text(encoding='utf-8'))
    OUT=(ROOT/'renders'/CONFIG.get('output_dir','seedance25')).resolve()
    if not OUT.is_relative_to((ROOT/'renders').resolve()):
        p.error('Output must stay inside video/renders')
    try:
        for sid in args.shots:
            globals()[args.action](next(s for s in CONFIG['shots'] if s['id']==sid))
    except Exception as error:
        print(str(error) if isinstance(error,(RuntimeError,AssertionError)) else type(error).__name__)
        raise SystemExit(1)
