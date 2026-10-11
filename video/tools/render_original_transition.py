"""v04: owner's outline morph, real speech envelope, native-speed voices.

Adapted locally from reviewed references/motion/original-source/voxwave_render.py.
No network calls. Original sources stay unchanged; geometry is canonical SVG.
"""
import array
import bisect
import hashlib
import json
import math
import random
import subprocess
from PIL import Image, ImageDraw
import render_brand_transition as base
import render_opening_variants as body
from render_opening_animatic import OUT, ROOT, W, H, FPS, run

RATE = base.RATE
START = 56
END = 69
AA = 2
KEYS = ['coral', 'navy', 'teal']
STROKES = [(255,110,66), (9,38,52), (0,78,114)]
sm = base.ease


def contour(points, n=360):
    points = points + [points[0]]
    lengths = [0.]
    for a,b in zip(points, points[1:]):
        lengths.append(lengths[-1] + math.dist(a,b))
    result = []
    for j in range(n):
        at = j*lengths[-1]/n
        k = min(len(points)-2, bisect.bisect_right(lengths,at)-1)
        f = (at-lengths[k])/(lengths[k+1]-lengths[k])
        result.append(tuple(a+(b-a)*f for a,b in zip(points[k],points[k+1])))
    area = sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(result,result[1:]+result[:1]))
    if area<0: result.reverse()
    left = min(range(n),key=lambda i:result[i][0])
    result = result[left:]+result[:left]
    normals=[]
    for i in range(n):
        x = result[(i+3)%n][0]-result[(i-3)%n][0]
        y = result[(i+3)%n][1]-result[(i-3)%n][1]
        length = math.hypot(x,y) or 1
        normals.append((-y/length,x/length))
    return result,normals


def smooth_closed(points):
    out=[]
    for i,p in enumerate(points):
        before=points[i-1]; after=points[(i+1)%len(points)]
        a=((before[0]+p[0])/2,(before[1]+p[1])/2)
        b=((after[0]+p[0])/2,(after[1]+p[1])/2)
        for u in (0, .5):
            out.append(tuple((1-u)**2*a[k]+2*(1-u)*u*p[k]+u*u*b[k] for k in (0,1)))
    return out+[out[0]]


def audio():
    # Whole conversation stays intact: no cuts, inserted reply gaps or time stretch.
    raw=base.decode(OUT/'opening-dialogue-v03-raw.mp3')
    run('-y','-i',str(OUT/'opening-dialogue-v03-raw.mp3'),'-af',
        'highpass=f=300,lowpass=f=3400','-ar',str(RATE),'-ac','1',
        str(OUT/'opening-dialogue-v03-phone.wav'))
    call=base.decode(OUT/'opening-dialogue-v03-phone.wav')
    phone=array.array('h',[0])*(END*RATE)
    phone[3*RATE:3*RATE+len(call)]=call
    narrator=base.decode(OUT/'brand-narration-v02-raw.mp3')
    meta=json.loads((OUT/'brand-narration-v02-timestamps.json').read_text(encoding='utf-8-sig'))
    boundary=round(meta['voice_segments'][1]['start_time_seconds']*RATE)
    narration=array.array('h',[0])*(END*RATE)
    cues=[]
    for at,clip in ((57.6,narrator[:boundary]),(62.8,narrator[boundary:])):
        i=round(at*RATE); narration[i:i+len(clip)]=clip
        cues.append({'start':at,'end':at+len(clip)/RATE,'speed':1})
    base.save_wav(OUT/'brand-narration-v02-timed.wav',narration)
    rng=random.Random(40); air=0.; swish=0.; mix=array.array('h')
    for i in range(END*RATE):
        t=i/RATE
        air=.995*air+.005*rng.uniform(-1,1)
        swish=.88*swish+.12*rng.uniform(-1,1)
        overall=sm(0,2,t)*(1-sm(67,69,t))
        duck=.48 if any(c['start']-.2<t<c['end']+.3 for c in cues) else 1
        pad=sum(a*math.sin(2*math.pi*f*t) for f,a in ((146.8324,36),(220,26),(329.6276,16),(440,8)))
        movement=sm(61.1,62.6,t)*(1-sm(64.6,66,t))
        movement*=.55 if 62.6<t<64.5 else 1
        elapsed=max(0,t-64.8)
        bell=0 if t<64.8 else math.exp(-elapsed*2.3)*sm(64.8,64.85,t)
        organic=swish*700*movement+bell*(115*math.sin(2*math.pi*440*elapsed)+55*math.sin(2*math.pi*660*elapsed))
        ring=0
        if .2<t<.75 or 1.1<t<1.65:
            u=(t-.2) if t<.75 else (t-1.1)
            ring=1500*min(1,u/.02,(.55-u)/.03)*math.sin(2*math.pi*440*t)
        value=phone[i]*.27+narration[i]*.82+(air*650+pad*duck)*overall+organic*3+ring
        assert abs(value)<32767
        mix.append(round(value))
    base.save_wav(OUT/'opening-animatic-v04-soft.wav',mix)
    # Existing body renderer expects 30 fps envelope values, independent of sample rate.
    levels,dt=base.envelope(phone)
    body_levels=[levels[min(len(levels)-1,int(i/FPS/dt))] for i in range(END*FPS)]
    return narration,body_levels,cues,3+len(raw)/RATE


def render_tail(symbols,letters,narration,output_path=None,envelope_fn=None,inertia_release=1.25,stroke_start=16*2/3):
    contours=[contour(symbols[k]) for k in KEYS]
    levels,dt=(envelope_fn or base.envelope)(narration)
    # Give the drawn line inertia across a natural spoken pause, rather than
    # stretching the recording or replacing its envelope with invented syllables.
    inertia=0.
    for i,level in enumerate(levels) if inertia_release is not None else []:
        inertia+=(level-inertia)*(1-math.exp(-dt/(.08 if level>inertia else inertia_release)))
        levels[i]=inertia
    def amplitude(k,u,t):
        delay=[0,.08,.16][k]
        level=levels[max(0,min(len(levels)-1,int((START+t-delay)/dt)))]
        phase=[0,1.7,3.1][k]
        center=.5+[0,-.06,.07][k]+.05*math.sin(.8*t+k*2)
        window=math.exp(-((u-center)/[.19,.23,.16][k])**2)
        a=.5+.5*math.sin([3.2,2.6,3.9][k]*2*math.pi*(u-center)+1.3*math.sin(1.7*t+phase)+phase)
        b=.5+.5*math.sin([6.5,5.3,7.4][k]*2*math.pi*(u-center)-1.1*math.sin(1.1*t+2*phase))
        return 200*level*window*(.62*a+.38*b)
    path=output_path or OUT/'opening-animatic-v04-tail.mp4'
    cmd=['ffmpeg','-hide_banner','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
        '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264',
        '-crf','18','-preset','fast','-pix_fmt','yuv420p',str(path)]
    hold=None
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for frame in range((END-START)*FPS):
            t=frame/FPS
            # Extend the original pre-morph motion by 1.2 seconds.
            r=t-1.2
            bg=round(249*sm(6.1,7.1,r))
            im=Image.new('RGB',(W*AA,H*AA),(bg,bg,bg))
            fill=sm(6.4,7.2,r)
            if fill:
                layer=im.copy(); draw=ImageDraw.Draw(layer)
                for k in ('navy','teal','coral'):
                    draw.polygon([(x*AA,y*AA) for x,y in symbols[k]],fill=base.COLORS[k])
                im=Image.blend(im,layer,fill)
            for index,(bbox,key,mask) in enumerate(letters):
                progress=sm(8.1+index*.13,9.05+index*.13,t)
                if progress:
                    offset=round(26*AA*(1-progress))
                    im.paste(base.COLORS[key],(bbox[0],bbox[1]+offset),mask.point(lambda x:round(x*progress)))
            visibility=[1,sm(1.8,3,t),sm(2.2,3.4,t)]
            sync=sm(4,5.2,r); damp=1-.6*sm(4.6,5.8,r)
            q=sm(4.5,6.4,r)
            p=4*q**3 if q<.5 else 1-(-2*q+2)**3/2
            width=stroke_start*(1-q)+(2*2/3)*q
            baseline=548-188*sm(0,.9,t)
            for k in (1,2,0):
                opacity=visibility[k]*(1-sm(6.8,7.4,r))
                if opacity<=0: continue
                points=[]; target,normals=contours[k]
                for j in range(360):
                    side=-1 if j<=180 else 1
                    u=(j if j<=180 else 360-j)/180
                    amp=amplitude(k,u,t)
                    amp+=(amplitude(0,u,t)-amp)*sync
                    amp*=damp*visibility[k]
                    x=320+640*u; y=baseline+side*amp
                    tx=target[j][0]+normals[j][0]*width/2
                    ty=target[j][1]+normals[j][1]*width/2
                    points.append((x+(tx-x)*p,y+(ty-y)*p))
                layer=im.copy()
                ImageDraw.Draw(layer).line([(x*AA,y*AA) for x,y in smooth_closed(points)],
                    fill=STROKES[k],width=max(1,round(width*AA)),joint='curve')
                im=Image.blend(im,layer,opacity)
            im=im.resize((W,H),Image.Resampling.LANCZOS)
            if output_path is None and frame in (60,100,150,185,210,230,255,300,360):
                im.save(OUT/f'v04-logo-{frame:03}.png')
            if t>=11:
                digest=hashlib.sha256(im.tobytes()).hexdigest()
                if hold is None: hold=digest
                assert digest==hold, 'Final logo must stay still'
            proc.stdin.write(im.tobytes())
        proc.stdin.close(); assert proc.wait()==0
    return path


def main():
    # Match original scale and centering, not the rejected v03 enlargement.
    base.screen=lambda p:(W/2+(p[0]-627)*.7*2/3,H/2+(p[1]-635)*.7*2/3)
    symbols,letters,digest=base.load_geometry()
    narration,levels,cues,call_end=audio()
    tail=render_tail(symbols,letters,narration)
    # Reuse shot/card layout, but regenerate all waveforms against the NEW audio.
    body.OUT=OUT/'v04-body'
    body.OUT.mkdir(exist_ok=True)
    body_path=body.render_body('A',levels,Image.new('RGB',(W,H),'black'))
    visual=OUT/'opening-animatic-v04-visual.mp4'
    run('-y','-i',str(body_path),'-i',str(tail),'-filter_complex',
        '[0:v]trim=end_frame=1680,setpts=PTS-STARTPTS[b];[b][1:v]concat=n=2:v=1:a=0[v]',
        '-map','[v]','-an','-c:v','libx264','-crf','18','-preset','fast',str(visual))
    final=OUT/'opening-animatic-v04-soft.mp4'
    run('-y','-i',str(visual),'-i',str(OUT/'opening-animatic-v04-soft.wav'),
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final))
    run('-y','-ss','50','-i',str(final),'-c:v','libx264','-crf','18','-preset','fast',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'logo-comparison-v04-soft.mp4'))
    (OUT/'opening-animatic-v04-verification.json').write_text(json.dumps({
        'duration':END,'narration':cues,'call_end':call_end,'question_start':50,
        'native_audio_speed':True,'inserted_conversation_gaps':0,
        'canonical_sha256':digest,'morph_start':61.7,'morph_end':63.6,
        'fill_start':63.6,'fill_end':64.4,'official_letters':len(letters),
        'source':'Owner supplied original outline animation; local adaptation',
        'note':'All four cinematic shots are still labelled storyboard placeholders.'
    },indent=2),encoding='utf-8')
    print('v04 complete; call ends at',call_end,'narration',cues,flush=True)


if __name__=='__main__': main()
