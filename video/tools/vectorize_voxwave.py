from pathlib import Path
from collections import defaultdict
import json
import argparse
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Vectorize a supplied VoxWave source image.')
parser.add_argument('input', type=Path, help='Path to the original raster logo image')
parser.add_argument('--output-dir', type=Path, default=ROOT/'renders/drafts/vectorized-logo')
args=parser.parse_args()
OUT=args.output_dir
OUT.mkdir(parents=True, exist_ok=True)
im=np.array(Image.open(args.input).convert('RGB'))
palette=np.array([[249,249,249],[9,43,60],[2,83,124],[255,101,60]])
labels=np.argmin(((im.astype(float)[:,:,None,:]-palette[None,None,:,:])**2).sum(axis=3),axis=2)

def contours(mask):
    # Oriented cell boundaries preserve both exterior outlines and counters.
    edges=defaultdict(list)
    h,w=mask.shape
    for y,x in zip(*np.where(mask)):
        if y==0 or not mask[y-1,x]: edges[(x,y)].append((x+1,y))
        if x==w-1 or not mask[y,x+1]: edges[(x+1,y)].append((x+1,y+1))
        if y==h-1 or not mask[y+1,x]: edges[(x+1,y+1)].append((x,y+1))
        if x==0 or not mask[y,x-1]: edges[(x,y+1)].append((x,y))
    result=[]
    while edges:
        first=next(iter(edges)); p=first; ring=[]
        while True:
            ring.append(p)
            nxt=edges[p].pop()
            if not edges[p]: del edges[p]
            p=nxt
            if p==first: break
        if len(ring)>30:
            a=np.array(ring,dtype=float)
            area=abs(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1)))/2
            if area>20: result.append(a)
    return result

def unit(v):
    return v/max(np.linalg.norm(v),1e-12)

def fit(p,t1,t2,tol=.65):
    if len(p)==2:
        d=np.linalg.norm(p[-1]-p[0])/3
        return [(p[0]+d*t1,p[-1]+d*t2,p[-1])]
    u=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
    u=u/u[-1]; v=1-u
    b0=v**3; b1=3*u*v*v; b2=3*u*u*v; b3=u**3
    a=np.stack([b1[:,None]*t1,b2[:,None]*t2],axis=2).reshape(-1,2)
    rhs=(p-(b0+b1)[:,None]*p[0]-(b2+b3)[:,None]*p[-1]).reshape(-1)
    alpha=np.linalg.lstsq(a,rhs,rcond=None)[0]
    d=np.linalg.norm(p[-1]-p[0])
    if min(alpha)<1e-5 or max(alpha)>max(d*4,10): alpha[:]=d/3
    c1=p[0]+alpha[0]*t1; c2=p[-1]+alpha[1]*t2
    q=b0[:,None]*p[0]+b1[:,None]*c1+b2[:,None]*c2+b3[:,None]*p[-1]
    errors=np.linalg.norm(q-p,axis=1); k=int(np.argmax(errors))
    if errors[k]<=tol: return [(c1,c2,p[-1])]
    k=max(1,min(len(p)-2,k)); tangent=unit(p[max(k-2,0)]-p[min(k+2,len(p)-1)])
    return fit(p[:k+1],t1,tangent,tol)+fit(p[k:],-tangent,t2,tol)

def fmt(p): return f'{p[0]:.2f},{p[1]:.2f}'
def path(ring):
    # Subpixel smoothing removes the raster staircase before curve fitting.
    p=sum(np.roll(ring,k,axis=0)*v for k,v in [(-2,1),(-1,2),(0,3),(1,2),(2,1)])/9
    segments=[]; n=len(p)
    for a,b in zip([0,n//4,n//2,3*n//4],[n//4,n//2,3*n//4,n]):
        pts=np.vstack([p[a:b],p[b%n]])
        t1=unit(p[(a+2)%n]-p[(a-2)%n]); t2=unit(p[(b-2)%n]-p[(b+2)%n])
        segments+=fit(pts,t1,t2)
    return 'M'+fmt(p[0])+' '.join(' C'+fmt(a)+' '+fmt(b)+' '+fmt(c) for a,b,c in segments)+' Z'

groups=[]; stats={}
for idx,name in [(1,'Azul-marino'),(2,'Azul'),(3,'Naranja')]:
    rings=contours(labels==idx)
    color='#'+''.join(f'{int(x):02x}' for x in np.median(im[labels==idx],axis=0))
    symbol=[r for r in rings if r[:,1].mean()<750]
    letters=[r for r in rings if r[:,1].mean()>=750]
    parts=[]
    for role,rs in [('Simbolo',symbol),('Letras',letters)]:
        if rs: parts.append(f'<path id="{role}-{name}" fill="{color}" fill-rule="evenodd" d="'+ ' '.join(path(r) for r in rs)+'"/>')
    groups.extend(parts); stats[name]={'color':color,'contours':len(rings)}

def svg(view,background=False):
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-labelledby="title desc">\n<title id="title">VoxWave</title>\n<desc id="desc">Logotipo vectorizado con curvas editables. Letras convertidas a trazados para conservar su forma sin depender de fuentes.</desc>\n'+ ('<rect id="Fondo" width="1254" height="1254" fill="#f9f9f9"/>\n' if background else '')+'\n'.join(groups)+'\n</svg>\n'
(OUT/'VoxWave-editable.svg').write_text(svg('120 327 1024 620'),encoding='utf-8')
(OUT/'VoxWave-original-layout.svg').write_text(svg('0 0 1254 1254',True),encoding='utf-8')
print(json.dumps(stats))
