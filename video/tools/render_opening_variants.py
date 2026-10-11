"""Local v02 comparison: slower shots, smooth waveform, two endings/two beds.

No paid generation. Existing dialogue is left intact; synthetic music/air beds
are provisional sound-design sketches. Run from any directory.
"""
import array
import json
import math
import random
import subprocess
import wave
from PIL import Image, ImageDraw
from render_opening_animatic import OUT, ROOT, W, H, FPS, ORANGE, card, placeholder, run

DURATION = 63
LOGO_START = 57
QUESTION_START = {'A': 50, 'B': 47}


def smoothstep(x):
    x = min(1, max(0, x))
    return x*x*(3-2*x)


def load_audio(path):
    with wave.open(str(path),'rb') as f:
        assert (f.getnchannels(),f.getsampwidth(),f.getframerate()) == (1,2,44100)
        return array.array('h',f.readframes(f.getnframes()))


def envelope(samples):
    hop=1470
    raw=[math.sqrt(sum(v*v for v in samples[i:i+hop])/hop)/32768
         for i in range(0,len(samples),hop)]
    scale=sorted(raw)[round(.97*len(raw))]
    result=[]
    value=0
    for i in range(DURATION*FPS):
        target=min(1,raw[i]/scale) if i<len(raw) else 0
        # Broad attack and release: volume-driven motion without syllable jitter.
        tau=.22 if target>value else .55
        value+=(target-value)*(1-math.exp(-1/(FPS*tau)))
        result.append(value)
    assert max(result[:85])==0 and result[56*FPS]<.001
    return result


def draw_wave(image,t,level):
    p=smoothstep((t-55.7)/.85)
    baseline=548-188*p
    d=ImageDraw.Draw(image)
    for sign in (1,-1):
        points=[]
        for j in range(321):
            u=j/320
            # Smooth analytic shape; only its envelope follows the real speech.
            shape=math.exp(-((u-.5)/.20)**2)*math.sin(u*math.pi*4.0+t*.8)
            points.append((320+640*u,baseline+sign*level*65*shape))
        d.line(points,fill=ORANGE,width=6,joint='curve')
    for x in (320,960):
        d.ellipse((x-3,baseline-3,x+3,baseline+3),fill=ORANGE)


def make_beds():
    speech=load_audio(OUT/'opening-dialogue-v02-preview-50s.wav')
    rng=random.Random(20261010)
    air=0.0
    mixes={name:array.array('h') for name in ('ambience','music')}
    for i in range(DURATION*44100):
        t=i/44100
        voice=speech[i]*(.6 if t<3 else .27) if i<len(speech) else 0
        fade=smoothstep(t/2)*(1-smoothstep((t-60)/3))
        air=.995*air+.005*rng.uniform(-1,1)
        outdoor=1+.8*smoothstep((t-27)/1)*(1-smoothstep((t-32)/1))
        ambient=air*650*outdoor*fade
        # A quiet sustained open chord, no beat, melody, borrowed recording or sample.
        frequencies=(146.8324,220.0,329.6276,440.0)
        pad=sum(math.sin(2*math.pi*f*t+.08*math.sin(t*.17+j))*a
                for j,(f,a) in enumerate(zip(frequencies,(36,26,16,8))))
        pad*=fade*(.85+.15*math.sin(t*.31))
        mixes['ambience'].append(round(voice+ambient))
        mixes['music'].append(round(voice+pad+ambient*.25))
    for name,samples in mixes.items():
        assert len(samples)==DURATION*44100 and max(abs(v) for v in samples)<32767
        with wave.open(str(OUT/f'animatic-v02-{name}.wav'),'wb') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(44100)
            f.writeframes(samples.tobytes())


def render_body(ending,levels,first_logo):
    question_start=QUESTION_START[ending]
    cards=[
        (6,11,card([('More than 10 million',57,True),('people worldwide live with',43,False),
                    ('Parkinson’s disease',47,False)],["Parkinson’s Foundation · Global estimate"])),
        (16,27,card([('Parkinson’s is the fastest-growing',43,True),
                    ('neurological condition in the world,',43,False),
                    ('with global cases projected to reach',43,False),('over 25 million by 2050.',49,True)],
                   ['BMJ, 2025 · Projection based on GBD 2021',
                    'Growth ranking: prevalence and disability, GBD 2015'])),
        (32,37,card([('Symptoms can appear',49,False),('long before',57,True),
                    ('they are recognised.',49,False)],["Parkinson’s UK · Diagnosis information"])),
        (42,question_start,card([('Seeing a specialist can mean',47,False),('months of waiting',57,True)],
                    ['Lithuania specialist-care survey · LRT / Baltijos tyrimai, 2025'])),
        (question_start,56,card([('What if the answer was',50,False),('always there?',59,True)],[]))]
    shots=[(0,6,placeholder(1,'THE CALL','Close-up · A hand answers a button mobile · No face')),
           (11,16,placeholder(2,'AT HOME','Hallway, window, armchair, blanket and a single cup')),
           (27,32,placeholder(3,'THE DISTANCE','An empty rural Baltic road · Locked wide shot')),
           (37,42,placeholder(4,'THE WAIT','Waiting chairs and a closed consultation-room door'))]
    ranges=sorted([(a,b) for a,b,_ in cards+shots]+[(56,57)])
    assert ranges[0][0]==0 and ranges[-1][1]==57
    assert all(a[1]==b[0] for a,b in zip(ranges,ranges[1:]))
    assert all(b-a>=5 for a,b,_ in shots)
    path=OUT/f'opening-animatic-v02-{ending}-body.mp4'
    cmd=['ffmpeg','-hide_banner','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264',
         '-preset','fast','-crf','19','-pix_fmt','yuv420p',str(path)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as p:
        for frame in range(LOGO_START*FPS):
            t=frame/FPS
            image=Image.new('RGB',(W,H),'black')
            for a,b,base in shots:
                if a<=t<b:
                    image=base.copy()
            for a,b,base in cards:
                if a<=t<b:
                    opacity=min(1,(t-a)/.4,(b-t)/.3)
                    image=Image.blend(image,base,max(0,opacity))
                    draw_wave(image,t,levels[frame])
            if 56<=t<57:
                draw_wave(image,t,levels[frame])
            # Match the actual reference image before playback, avoiding a hard jump.
            if t>=56.55:
                image=Image.blend(image,first_logo,smoothstep((t-56.55)/.45))
            if frame in (540,990,1455,1515,1665,1707):
                image.save(OUT/f'v02-{ending}-{frame}.jpg',quality=92)
            p.stdin.write(image.tobytes())
            if frame%600==0: print(f'{ending}: {frame}/{LOGO_START*FPS}',flush=True)
        p.stdin.close()
        assert p.wait()==0
    return path


def main():
    ref=ROOT/'references/motion/voxwave_logo_reveal DEFINITIVO.mp4'
    logo=OUT/'opening-animatic-v02-logo.mp4'
    run('-y','-i',str(ref),'-vf',
        f'trim=start_frame=106:end_frame=286,setpts=PTS-STARTPTS,scale={W}:{H},fps={FPS}',
        '-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p',str(logo))
    first=OUT/'v02-logo-first.png'
    run('-y','-i',str(logo),'-frames:v','1',str(first))
    levels=envelope(load_audio(OUT/'opening-dialogue-v02-phone-50s.wav'))
    print('Preparing provisional sound beds',flush=True)
    make_beds()
    for ending in ('A','B'):
        body=render_body(ending,levels,Image.open(first).convert('RGB'))
        visual=OUT/f'opening-animatic-v02-{ending}-visual.mp4'
        run('-y','-i',str(body),'-i',str(logo),'-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]',
            '-map','[v]','-an','-c:v','libx264','-crf','19','-preset','fast',str(visual))
        for bed in ('ambience','music'):
            run('-y','-i',str(visual),'-i',str(OUT/f'animatic-v02-{bed}.wav'),
                '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k',
                '-movflags','+faststart',str(OUT/f'opening-animatic-v02-{ending}-{bed}.mp4'))
    (OUT/'opening-animatic-v02-settings.json').write_text(json.dumps({
        'duration':DURATION,'question_start':QUESTION_START,'logo_start':LOGO_START,
        'dialogue_last_segment_end':49.75,'dialogue_gain':.27,
        'waveform_attack_seconds':.22,'waveform_release_seconds':.55,
        'waveform_stroke_px':6,'shot_durations':[6,5,5,5],
        'sound_beds':'Local provisional syntheses, not final sound design'
    },indent=2),encoding='utf-8')
    print('Four comparison exports complete',flush=True)


if __name__=='__main__':
    main()
