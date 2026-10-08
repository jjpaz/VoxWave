from pathlib import Path
import re, math, subprocess, json
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'renders/drafts/logo-reveal'
OUT.mkdir(parents=True, exist_ok=True)
W,H,FPS,SECONDS,AA=1920,1080,30,8,2
COLORS={'Azul-marino':(10,42,59),'Azul':(2,82,125),'Naranja':(254,101,60)}

def ease(a,b,t):
    q=np.clip((t-a)/(b-a),0,1)
    return q*q*q*(q*(q*6-15)+10)

def parse(d):
    tokens=re.findall(r'[MCZ]|-?\d+(?:\.\d+)?',d)
    rings=[]; pts=[]; i=0; p=None
    while i<len(tokens):
        c=tokens[i]; i+=1
        if c=='M':
            p=np.array([float(tokens[i]),float(tokens[i+1])]); i+=2; pts=[p]
        elif c=='C':
            a,b,e=np.array(list(map(float,tokens[i:i+6]))).reshape(3,2); i+=6
            n=max(3,int((np.linalg.norm(a-p)+np.linalg.norm(b-a)+np.linalg.norm(e-b))/2))
            for u in np.linspace(0,1,n+1)[1:]:
                pts.append((1-u)**3*p+3*(1-u)**2*u*a+3*(1-u)*u*u*b+u**3*e)
            p=e
        elif c=='Z': rings.append(np.array(pts)); pts=[]
    return rings

def screen(p): return (p-np.array([632,636.5]))*.96+np.array([960,540])
paths={}
for el in ET.parse(ROOT/'assets/logo/VoxWave-vector/VoxWave-animation-source.svg').getroot():
    if el.tag.endswith('path'): paths[el.attrib['id']]=[screen(r) for r in parse(el.attrib['d'])]

def poly_mask(rings):
    result=Image.new('1',(W*AA,H*AA))
    for r in rings:
        layer=Image.new('1',result.size)
        ImageDraw.Draw(layer).polygon([tuple(p) for p in r*AA],fill=1)
        result=ImageChops.logical_xor(result,layer)
    return result.convert('L')

letters={key:poly_mask(paths['Letras-'+key]) for key in ['Azul-marino','Azul']}
symbols={key:paths['Simbolo-'+key][0] for key in COLORS}

def split_ring(r):
    left=np.argmin(r[:,0]); r=np.roll(r,-left,axis=0); right=np.argmax(r[:,0])
    sides=[r[:right+1],np.vstack([r[right:],r[0]])[::-1]]
    if sides[0][:,1].mean()>sides[1][:,1].mean(): sides=sides[::-1]
    return sides
sides={k:split_ring(r) for k,r in symbols.items()}

def speech(x,t,ch):
    # Uneven syllable envelopes and mixed harmonics with natural pauses.
    z=x-0.43*t+ch*.021
    env=np.zeros_like(x)
    for center,amp,width in [(-2,.65,.13),(-1.68,1,.085),(-1.39,.5,.055),(-1.05,.95,.12),(-.79,.55,.045),(-.5,.9,.09),(-.21,.6,.065),(.10,1,.10),(.35,.65,.055),(.58,.9,.09),(.86,.45,.06)]:
        env+=amp*np.exp(-((z-center)/width)**2)
    carrier=(np.sin(2*np.pi*(8.3*z+1.6*z*z)+ch*.4)+.37*np.sin(2*np.pi*18.8*z+1.3+ch*.2)+.16*np.sin(2*np.pi*31.7*z+.6))/1.4
    window=np.sin(np.pi*np.clip(x,0,1))**.65
    return 106*env*carrier*window*ease(.8,1.4,t)

def contour(key,t,ch):
    m=ease(4.45,6.08,t)
    result=[]
    target=symbols[key]; lo=target[:,0].min(); span=np.ptp(target[:,0])
    for idx,side in enumerate(sides[key]):
        u=np.clip((side[:,0]-lo)/span,0,1)
        v=speech(u,t,ch)
        dx=0.0005
        slope=(speech(np.minimum(u+dx,1),t,ch)-speech(np.maximum(u-dx,0),t,ch))/(2*dx*1080)
        n=np.sqrt(1+slope*slope)
        sign=-1 if idx==0 else 1
        origin=np.column_stack([420+1080*u-sign*6*slope/n,540+v+sign*6/n])
        # Curves themselves travel into the exact vector outline.
        points=origin*(1-m)+side*m
        result.append(points if idx==0 else points[::-1])
    return np.vstack(result)

ffmpeg='ffmpeg'
cmd=[ffmpeg,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'VoxWave-reveal.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
samples=[]
last=None; hold_equal=True
for frame in range(FPS*SECONDS):
    t=frame/FPS
    bg=round(249*ease(2.45,5.7,t))
    im=Image.new('RGB',(W*AA,H*AA),(bg,bg,bg))
    for ch,key in [(2,'Azul-marino'),(1,'Azul'),(0,'Naranja')]:
        alpha=ease(.13,.48,t) if ch==0 else ease(1.65+(2-ch)*.38,2.3+(2-ch)*.38,t)
        if alpha>0:
            mask=Image.new('L',im.size)
            r=symbols[key] if t>=6.08 else contour(key,t,ch)
            ImageDraw.Draw(mask).polygon([tuple(p) for p in r*AA],fill=round(alpha*255))
            im.paste(COLORS[key],(0,0),mask)
    a=ease(5.7,6.5,t)
    if a>0:
        for key,mask in letters.items(): im.paste(COLORS[key],(0,0),mask if a>=1 else mask.point(lambda x:round(x*a)))
    im=im.resize((W,H),Image.Resampling.LANCZOS)
    data=im.tobytes(); proc.stdin.write(data)
    if frame>=195:
        if last is not None: hold_equal=hold_equal and last==data
        last=data
    if frame in [0,18,49,82,120,154,177,195]:
        samples.append((t,im.copy()))
    if frame%30==0: print(f'Rendered {frame//30}/{SECONDS} seconds',flush=True)
proc.stdin.close()
if proc.wait()!=0: raise RuntimeError('Video encoder failed')
im.save(OUT/'VoxWave-final.png')
sheet=Image.new('RGB',(960*2,580*4),'#e7e7e7')
d=ImageDraw.Draw(sheet)
for j,(t,img) in enumerate(samples):
    x=(j%2)*960;y=(j//2)*580
    sheet.paste(img.resize((960,540)),(x,y)); d.text((x+20,y+552),f'{t:.2f} s',fill='black')
sheet.save(OUT/'VoxWave-storyboard.jpg',quality=90)
subprocess.run([ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(OUT/'VoxWave-reveal.mp4'),'-filter_complex','fps=12,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(OUT/'VoxWave-preview.gif')],check=True)
(OUT/'verification.json').write_text(json.dumps({'duration_seconds':SECONDS,'fps':FPS,'size':[W,H],'final_hold_seconds':1.5,'final_hold_identical_frames':hold_equal,'colors':COLORS},indent=2))
print('Complete. Final hold identical:',hold_equal)
