"""New voice-reactive logo morph, official SVG geometry, two sound designs.

Local rendering only. Requires the existing v02 A body, dialogue and generated
George narration. Never calls an API or changes the source logo.
"""
import array
import hashlib
import json
import math
import random
import re
import subprocess
import wave
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageChops
from render_opening_animatic import ROOT, OUT, W, H, FPS, run
from render_opening_variants import smoothstep

RATE=22050
DURATION=69
AA=2
SCALE=.58
COLORS={'navy':(10,42,59),'teal':(2,82,125),'coral':(254,101,60)}


def ease(a,b,t):
    return smoothstep((t-a)/(b-a))


def decode(path):
    result=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(path),
        '-f','s16le','-ac','1','-ar',str(RATE),'pipe:1'],capture_output=True,check=True)
    return array.array('h',result.stdout)


def save_wav(path,samples):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE)
        f.writeframes(samples.tobytes())


def parse_path(d):
    """Flatten only the canonical logo's M/L/C/Z SVG command subset."""
    tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?',d)
    rings=[]; points=[]; p=(0.,0.); start=p; cmd=None; i=0
    while i<len(tokens):
        if tokens[i].isalpha():
            cmd=tokens[i]; i+=1
            if cmd.upper()=='Z':
                if points: rings.append(points)
                points=[]; p=start; cmd=None
                continue
        assert cmd and cmd.upper() in ('M','L','C'), f'Unsupported SVG command {cmd}'
        count=6 if cmd.upper()=='C' else 2
        nums=list(map(float,tokens[i:i+count])); i+=count
        relative=cmd.islower()
        pairs=[(nums[k]+(p[0] if relative else 0),nums[k+1]+(p[1] if relative else 0))
               for k in range(0,count,2)]
        if cmd.upper()=='M':
            if points: rings.append(points)
            p=pairs[0]; start=p; points=[p]; cmd='l' if relative else 'L'
        elif cmd.upper()=='L':
            p=pairs[0]; points.append(p)
        else:
            a,b,end=pairs
            length=sum(math.dist(x,y) for x,y in ((p,a),(a,b),(b,end)))
            steps=max(4,math.ceil(length/1.2))
            for j in range(1,steps+1):
                u=j/steps; v=1-u
                points.append((v**3*p[0]+3*v*v*u*a[0]+3*v*u*u*b[0]+u**3*end[0],
                               v**3*p[1]+3*v*v*u*a[1]+3*v*u*u*b[1]+u**3*end[1]))
            p=end
    if points: rings.append(points)
    return rings


def screen(p):
    return (W/2+(p[0]-632)*SCALE,H/2+(p[1]-638)*SCALE)


def load_geometry():
    canonical=ROOT/'assets/logo/VoxWave-vector/Logo-oficial.svg'
    paths={p.attrib['fill'].lower():p.attrib['d'] for p in ET.parse(canonical).getroot()
           if p.tag.endswith('path')}
    # Existing split paths preserve official letter counters. Verify every path
    # against the canonical source before using it, rather than retyping the logo.
    source=(ROOT/'voxwave-video-pitch/src/brand/logo.ts').read_text(encoding='utf-8')
    data=json.loads(source.split('export const LOGO = ',1)[1].split(' as const;',1)[0])
    for role in ('symbol','wordmark'):
        for key,items in data[role].items():
            color='#'+''.join(f'{c:02x}' for c in COLORS[key])
            for item in items:
                assert item in paths[color], 'Split logo differs from canonical SVG'
    symbols={key:[screen(p) for p in parse_path(items[0])[0]] for key,items in data['symbol'].items()}
    letters=[]
    for key,items in data['wordmark'].items():
        for item in items:
            rings=[[screen(p) for p in ring] for ring in parse_path(item)]
            mask=Image.new('1',(W*AA,H*AA))
            for ring in rings:
                part=Image.new('1',mask.size)
                ImageDraw.Draw(part).polygon([(round(x*AA),round(y*AA)) for x,y in ring],fill=1)
                mask=ImageChops.logical_xor(mask,part)
            bbox=mask.getbbox()
            assert bbox is not None
            letters.append((bbox,key,mask.convert('L').crop(bbox)))
    letters.sort(key=lambda item:item[0][0])
    assert len(letters)==7
    return symbols,letters,hashlib.sha256(canonical.read_bytes()).hexdigest()


def make_narration():
    raw=decode(OUT/'brand-narration-v01-raw.mp3')
    meta=json.loads((OUT/'brand-narration-v01-timestamps.json').read_text(encoding='utf-8-sig'))
    segments=meta['voice_segments']; assert len(segments)==2
    narration=array.array('h',[0])*(DURATION*RATE)
    cues=[]
    for i,(at,speed) in enumerate(((57.35,.80),(63.15,.92))):
        a=round(segments[i]['start_time_seconds']*RATE)
        b=round(segments[i+1]['start_time_seconds']*RATE) if i==0 else len(raw)
        clip=subprocess.run(['ffmpeg','-hide_banner','-v','error','-f','s16le','-ar',str(RATE),
            '-ac','1','-i','pipe:0','-af',f'atempo={speed}','-f','s16le','pipe:1'],
            input=raw[a:b].tobytes(),capture_output=True,check=True).stdout
        clip=array.array('h',clip)
        start=round(at*RATE)
        assert start+len(clip)<DURATION*RATE
        narration[start:start+len(clip)]=clip
        cues.append({'text':('In the voices we hear every day.','Meet VoxWave.')[i],
                     'start':at,'end':(start+len(clip))/RATE,'tempo':speed})
    assert cues[0]['end']<61.2 and 61.2<cues[1]['start']<65.1
    save_wav(OUT/'brand-narration-v01-timed.wav',narration)
    return narration,cues


def envelope(samples):
    # 10 ms input; smooth attack/release, genuine silence before/after voice.
    hop=round(RATE/100)
    raw=[math.sqrt(sum(x*x for x in samples[i:i+hop])/hop)/32768
         for i in range(0,len(samples),hop)]
    active=sorted(x for x in raw if x>.001)
    ref=active[int(.92*len(active))]
    result=[]; value=0
    for sample in raw:
        target=min(1.15,sample/ref)
        tau=.13 if target>value else .42
        value+=(target-value)*(1-math.exp(-hop/(RATE*tau)))
        result.append(value)
    return result,hop/RATE


def wave_y(u,t,amplitude,sign=1):
    return sign*amplitude*math.exp(-((u-.5)/.23)**2)*math.sin(u*math.pi*4+t*.8)


def split_ring(ring):
    left=min(range(len(ring)),key=lambda i:ring[i][0])
    r=ring[left:]+ring[:left]
    right=max(range(len(r)),key=lambda i:r[i][0])
    a=r[:right+1]; b=list(reversed(r[right:]+[r[0]]))
    if sum(p[1] for p in a)/len(a)>sum(p[1] for p in b)/len(b): a,b=b,a
    return a,b


def morph_ring(target,t,amount,amplitude,ch):
    sides=split_ring(target)
    lo=min(x for x,y in target); span=max(x for x,y in target)-lo
    ring=[]
    for index,side in enumerate(sides):
        points=[]
        for x,y in side:
            u=(x-lo)/span
            origin=(320+640*u,360+wave_y(u,t,amplitude,-1 if ch=='teal' else 1)+(-3 if index==0 else 3))
            points.append((origin[0]*(1-amount)+x*amount,origin[1]*(1-amount)+y*amount))
        ring.extend(points if index==0 else list(reversed(points)))
    return ring


def render_tail(symbols,letters,narration):
    levels,dt=envelope(narration)
    path=OUT/'opening-animatic-v03-tail.mp4'
    cmd=['ffmpeg','-hide_banner','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-crf','18',
         '-preset','fast','-pix_fmt','yuv420p',str(path)]
    hold=None
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for frame in range((DURATION-56)*FPS):
            t=56+frame/FPS
            bg=round(249*ease(62.5,64.7,t))
            im=Image.new('RGB',(W*AA,H*AA),(bg,bg,bg))
            amp=levels[min(len(levels)-1,int(t/dt))]*65
            m=ease(61.2,65.1,t)
            if t<60.7:
                baseline=548-188*ease(55.7,56.55,t)
                draw=ImageDraw.Draw(im)
                for sign in (1,-1):
                    pts=[((320+640*j/320)*AA,(baseline+wave_y(j/320,t,amp,sign))*AA) for j in range(321)]
                    draw.line(pts,fill=COLORS['coral'],width=6*AA,joint='curve')
            else:
                for key in ('navy','teal','coral'):
                    alpha=1 if key=='coral' else ease(60.7,61.7,t)
                    color=COLORS[key]
                    # Keep blue contours visible against black before the white reveal.
                    brightness=1-ease(62.5,64.7,t)
                    if key!='coral': color=tuple(round(v+(100-v)*brightness*.65) for v in color)
                    target=symbols[key]
                    ring=target if m>=1 else morph_ring(target,t,m,amp,key)
                    mask=Image.new('L',im.size)
                    ImageDraw.Draw(mask).polygon([(round(x*AA),round(y*AA)) for x,y in ring],fill=round(alpha*255))
                    im.paste(color,(0,0),mask)
            for i,(bbox,key,mask) in enumerate(letters):
                start=64.65+i*.15
                progress=ease(start,start+.85,t)
                if progress<=0: continue
                # Upward stagger with one soft overshoot; final SVG positions exact.
                offset=44*(1-progress)-7*math.sin(math.pi*progress)
                faded=mask if progress==1 else mask.point(lambda v:round(v*progress))
                im.paste(COLORS[key],(bbox[0],bbox[1]+round(offset*AA)),faded)
            im=im.resize((W,H),Image.Resampling.LANCZOS)
            if frame in (0,45,90,135,165,195,225,255,285,315,360,389):
                im.save(OUT/f'v03-logo-{frame:03d}.png')
            data=im.tobytes()
            if t>=67:
                if hold is not None: assert data==hold,'Final logo must hold still'
                hold=data
            proc.stdin.write(data)
            if frame%90==0: print(f'Logo tail {frame}/390',flush=True)
        proc.stdin.close(); assert proc.wait()==0
    return path


def mix_audio(narration,cues):
    speech=decode(OUT/'opening-dialogue-v02-preview-50s.wav')
    rng=random.Random(20261011)
    air=0.; swish=0.
    outputs={key:array.array('h') for key in ('organic','technology')}
    for i in range(DURATION*RATE):
        t=i/RATE
        call=speech[i]*(.6 if t<3 else .27) if i<len(speech) else 0
        voice=narration[i]*.82
        air=.995*air+.005*rng.uniform(-1,1)
        swish=.88*swish+.12*rng.uniform(-1,1)
        overall=ease(0,2,t)*(1-ease(67,69,t))
        duck=.48 if any(c['start']-.2<t<c['end']+.3 for c in cues) else 1.
        pad=sum(math.sin(2*math.pi*f*t)*a for f,a in ((146.8324,36),(220,26),(329.6276,16),(440,8)))
        pad*=overall*(.85+.15*math.sin(t*.31))*duck
        ambient=air*650*overall*(1+.8*ease(27,28,t)*(1-ease(32,33,t)))
        common=call+voice+pad+ambient
        movement=ease(60.7,62.2,t)*(1-ease(64.5,65.7,t))
        if 61<t<65:
            movement*=.55 if 63.0<t<64.8 else 1
        # One cohesive sound gesture under the letter wave, no per-letter clicks.
        elapsed=max(0,t-65.05)
        bell=0 if t<65.05 else math.exp(-elapsed*2.3)*ease(65.05,65.10,t)
        organic=swish*700*movement+bell*(115*math.sin(2*math.pi*440*elapsed)+55*math.sin(2*math.pi*660*elapsed))
        q=max(0,t-60.7)
        technology=movement*(90*math.sin(2*math.pi*(180*q+30*q*q))*(.7+.3*math.sin(q*math.pi*3)))
        technology+=bell*(80*math.sin(2*math.pi*880*elapsed)+45*math.sin(2*math.pi*1320*elapsed))
        outputs['organic'].append(round(common+organic*3))
        outputs['technology'].append(round(common+technology*3))
    for key,samples in outputs.items():
        assert len(samples)==DURATION*RATE and max(abs(v) for v in samples)<32767
        save_wav(OUT/f'opening-animatic-v03-{key}.wav',samples)


def main():
    symbols,letters,svg_hash=load_geometry()
    narration,cues=make_narration()
    print(json.dumps({'narrator':'George (temporary)','cues':cues}),flush=True)
    tail=render_tail(symbols,letters,narration)
    mix_audio(narration,cues)
    visual=OUT/'opening-animatic-v03-visual.mp4'
    run('-y','-i',str(OUT/'opening-animatic-v02-A-body.mp4'),'-i',str(tail),
        '-filter_complex','[0:v]trim=end_frame=1680,setpts=PTS-STARTPTS[body];[body][1:v]concat=n=2:v=1:a=0[v]',
        '-map','[v]','-an','-c:v','libx264','-crf','18','-preset','fast',str(visual))
    for key in ('organic','technology'):
        final=OUT/f'opening-animatic-v03-{key}.mp4'
        run('-y','-i',str(visual),'-i',str(OUT/f'opening-animatic-v03-{key}.wav'),
            '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final))
        run('-y','-ss','50','-i',str(final),'-c:v','libx264','-crf','18','-preset','fast',
            '-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/f'logo-comparison-v03-{key}.mp4'))
    (OUT/'opening-animatic-v03-verification.json').write_text(json.dumps({
        'duration':69,'narration':cues,'narrator':'George, temporary',
        'canonical_svg_sha256':svg_hash,'official_letters':len(letters),
        'morph_start':61.2,'morph_end':65.1,'letters_start':64.65,
        'letters_end':66.4,'final_hold_identical_after':67,
        'sound':'Both mixes combine locally synthesized ambience and pad. Only transition effect differs.'
    },indent=2),encoding='utf-8')
    print('New logo transition and both sound versions complete',flush=True)


if __name__=='__main__':
    main()
