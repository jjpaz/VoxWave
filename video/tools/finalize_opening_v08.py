"""Assemble the complete cinematic opening, smooth graphics and subdued audio.

Local only. Existing synthetic performances and source clips are preserved.
All source/intermediate/final media remain in ignored video/renders.
"""
import array
import json
import math
import random
import subprocess
import wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import render_brand_transition as base
import render_original_transition as logo
from render_opening_animatic import OUT, W, H, FPS, font, ORANGE, WHITE, run

WORK=OUT/'v08'
WORK.mkdir(exist_ok=True)
RATE=22050
QUESTION=53.2
TAIL=59.2
END=72.2
SHOTS=[(0,8.8),(13.8,18.8),(29.8,34.8),(39.8,44.8)]
CLIPS=[OUT/'seedance25-phone-v02/m01/m01-seedance25-v02.mp4']+[
    OUT/f'seedance25/m0{i}/m0{i}-seedance25-v01.mp4' for i in (2,3,4)]
CARDS=[
    (8.8,13.8,[('More than 10 million',57,True),('people worldwide live with',43,False),('Parkinson’s disease',47,False)],['Parkinson’s Foundation · Global estimate']),
    (18.8,29.8,[('Parkinson’s is the fastest-growing',43,True),('neurological condition in the world,',43,False),('with global cases projected to reach',43,False),('over 25 million by 2050.',49,True)],['BMJ, 2025 · Projection based on GBD 2021','Growth ranking: prevalence and disability, GBD 2015']),
    (34.8,39.8,[('Symptoms can appear',49,False),('long before',57,True),('they are recognised.',49,False)],['Parkinson’s UK · Diagnosis information']),
    (44.8,QUESTION,[('Seeing a specialist can mean',47,False),('months of waiting',57,True)],['Lithuania specialist-care survey · LRT / Baltijos tyrimai, 2025']),
    (QUESTION,TAIL,[('What if the answer was',50,False),('always there?',59,True)],[])]


def envelope(samples):
    """10 ms measured RMS; short smooth attack/release without long fake tails."""
    hop=round(RATE/100)
    raw=[math.sqrt(sum(v*v for v in samples[i:i+hop])/hop)/32768 for i in range(0,len(samples),hop)]
    active=sorted(x for x in raw if x>.001)
    ref=active[int(.92*len(active))]
    result=[]; value=0
    for v in raw:
        target=min(1.05,v/ref) if v>.001 else 0
        tau=.085 if target>value else .24
        value+=(target-value)*(1-math.exp(-hop/(RATE*tau)))
        if value<.0005:value=0
        result.append(value)
    return result,hop/RATE


def level_at(levels,dt,t):
    p=max(0,min(len(levels)-1,t/dt)); i=int(p)
    return levels[i]+(levels[min(i+1,len(levels)-1)]-levels[i])*(p-i)


def smooth_card(lines,sources):
    aa=3
    im=Image.new('RGB',(W*aa,H*aa),'black');d=ImageDraw.Draw(im)
    y=307-sum(size+17 for _,size,_ in lines)/2
    for text,size,bold in lines+[(s,16,False) for s in sources]:
        if size==16:y=637+sources.index(text)*23
        f=font(size*aa,bold); width=d.textlength(text,font=f)
        assert width<(W-130)*aa
        d.text(((W*aa-width)/2,y*aa),text,font=f,fill=WHITE if size!=16 else '#90979C')
        y+=size+17
    return im.resize((W,H),Image.Resampling.LANCZOS)


def draw_wave(image,t,level):
    # Rasterize vector-like curves at 4x, then reduce. Do not upscale old pixels.
    aa=4; left=312; top=464; width=656; height=168
    layer=Image.new('RGB',(width*aa,height*aa),'black');d=ImageDraw.Draw(layer)
    for sign in (-1,1):
        points=[]
        for j in range(1281):
            u=j/1280
            shape=math.exp(-((u-.5)/.20)**2)*math.sin(u*math.pi*4+(t-2.8)*.8)
            points.append(((8+640*u)*aa,(548-top+sign*level*65*shape)*aa))
        # A filled stroke outline avoids Pillow's tiny line-join notches when
        # many subpixel segments overlap on a very shallow curve.
        outside=[];inside=[]
        for j,(x,y) in enumerate(points):
            before=points[max(0,j-1)];after=points[min(len(points)-1,j+1)]
            dx=after[0]-before[0];dy=after[1]-before[1]
            length=math.hypot(dx,dy) or 1
            nx=-dy/length*3*aa;ny=dx/length*3*aa
            outside.append((x+nx,y+ny));inside.append((x-nx,y-ny))
        d.polygon(outside+inside[::-1],fill=ORANGE)
    for x in (8,648):d.ellipse(((x-3)*aa,(548-top-3)*aa,(x+3)*aa,(548-top+3)*aa),fill=ORANGE)
    image.paste(layer.resize((width,height),Image.Resampling.LANCZOS),(left,top))


def render_graphics(include_tail=True):
    speech=base.decode(OUT/'opening-dialogue-v02-phone-50s.wav')
    speech.extend(array.array('h',[0])*round((END-50)*RATE))
    levels,dt=envelope(speech)
    assert level_at(levels,dt,54)==0, 'Waveform must settle in post-call silence'
    cards=[(a,b,smooth_card(lines,sources)) for a,b,lines,sources in CARDS]
    target=WORK/'cards-aa.mp4'
    cmd=['ffmpeg','-hide_banner','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
         '-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p',str(target)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for frame in range(round(TAIL*FPS)):
            t=frame/FPS;im=Image.new('RGB',(W,H),'black')
            for a,b,card in cards:
                if a<=t<b:
                    opacity=max(0,min(1,(t-a)/.4,(b-t)/.3))
                    im=Image.blend(im,card,opacity)
                    level=level_at(levels,dt,t-2.8) if t>=5.8 else 0
                    draw_wave(im,t,level)
            if frame in (660,round(QUESTION*FPS)+30): im.save(WORK/f'graphics-{frame}.png')
            proc.stdin.write(im.tobytes())
            if frame%600==0:print('Graphics',frame,'/',round(TAIL*FPS),flush=True)
        proc.stdin.close();assert proc.wait()==0
    if not include_tail:return None
    # Preserve the owner's contour/colour/letter structure; improve edge quality
    # and remove the additional 1.25 s lag in voice-driven movement.
    base.AA=logo.AA=4
    base.screen=lambda p:(W/2+(p[0]-627)*.7*2/3,H/2+(p[1]-635)*.7*2/3)
    symbols,letters,digest=base.load_geometry()
    narration=base.decode(OUT/'brand-narration-v02-timed.wav')
    logo.render_tail(symbols,letters,narration,output_path=WORK/'tail.mp4',
                     envelope_fn=envelope,inertia_release=None,stroke_start=6)
    return digest


def write_wav(path,samples,rate=RATE):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(samples.tobytes())


def make_sound():
    # Generate only the local background bed/SFX. The performances are untouched.
    rng=random.Random(40);air=0.;swish=0.;bed=array.array('h')
    for i in range(round(END*RATE)):
        t=i/RATE;old=t-(TAIL-56)
        air=.995*air+.005*rng.uniform(-1,1)
        swish=.88*swish+.12*rng.uniform(-1,1)
        overall=base.ease(0,2,t)*(1-base.ease(END-2,END,t))
        duck=.48 if 60.6<t<63.6 or 65.8<t<68.1 else 1
        pad=sum(a*math.sin(2*math.pi*f*t) for f,a in ((146.8324,36),(220,26),(329.6276,16),(440,8)))
        movement=base.ease(61.1,62.6,old)*(1-base.ease(64.6,66,old))
        movement*=.55 if 62.6<old<64.5 else 1
        elapsed=max(0,old-64.8)
        bell=0 if old<64.8 else math.exp(-elapsed*2.3)*base.ease(64.8,64.85,old)
        organic=swish*700*movement+bell*(115*math.sin(2*math.pi*440*elapsed)+55*math.sin(2*math.pi*660*elapsed))
        bed.append(round((air*330+pad*duck)*overall+organic*2.1))
    write_wav(WORK/'bed.wav',bed)
    # Rebuild timed narration from its native recording at 48 kHz, preserving
    # both phrases, native pace and the original split between the phrases.
    raw=array.array('h',subprocess.check_output(['ffmpeg','-v','error','-i',str(OUT/'brand-narration-v02-raw.mp3'),'-f','s16le','-ac','1','-ar','48000','pipe:1']))
    meta=json.loads((OUT/'brand-narration-v02-timestamps.json').read_text(encoding='utf-8-sig'))
    boundary=round(meta['voice_segments'][1]['start_time_seconds']*48000)
    narrated=array.array('h',[0])*round(END*48000);cues=[]
    for at,clip in ((60.8,raw[:boundary]),(66.,raw[boundary:])):
        start=round(at*48000);narrated[start:start+len(clip)]=clip
        cues.append({'start':at,'end':at+len(clip)/48000})
    write_wav(WORK/'narrator.wav',narrated,48000)
    inputs=[OUT/'opening-dialogue-v02-phone-50s.wav',WORK/'narrator.wav',WORK/'bed.wav',
            OUT/'seedance25-phone-v02/m01/ringtone-synced.wav',*CLIPS]
    argv=[]
    for path in inputs:argv+=['-i',str(path)]
    common='aresample=48000,aformat=channel_layouts=stereo'
    filters=[f'[0:a]{common},acompressor=threshold=0.12:ratio=2:attack=15:release=180:makeup=1.5,volume=0.30,adelay=2800|2800,apad,atrim=duration={END},asplit=2[phone][duck]',
             f'[1:a]{common},volume=0.60[narr]',f'[2:a]{common}[bed]',f'[3:a]{common},volume=0.8[ring]']
    levels=[]
    for index,(clip,(a,b)) in enumerate(zip(CLIPS,SHOTS),4):
        pcm=base.decode(clip);rms=math.sqrt(sum(v*v for v in pcm)/len(pcm))/32768
        rms_db=20*math.log10(max(1e-9,rms));gain=min(0,-48-rms_db)
        levels.append({'shot':index-3,'source_rms_dbfs':rms_db,'gain_db':gain,'target_rms_dbfs':-48})
        filters.append(f'[{index}:a]{common},volume={gain}dB,volume=2,alimiter=limit=0.06324:level=0:latency=1,volume=0.5,apad,atrim=duration={b-a},afade=t=in:d=0.3,afade=t=out:st={min(b-a,8 if index==4 else 5)-.5}:d=0.5,adelay={round(a*1000)}|{round(a*1000)}[amb{index}]')
    filters+=['[amb4][amb5][amb6][amb7]amix=inputs=4:duration=longest:normalize=0[amb]',
              '[amb][duck]sidechaincompress=threshold=0.012:ratio=3:attack=30:release=350[quietamb]',
              f'[phone][narr][bed][ring][quietamb]amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.7943:level=0:latency=1,atrim=duration={END}[mix]']
    run('-y',*argv,'-filter_complex',';'.join(filters),'-map','[mix]','-ar','48000','-ac','2','-c:a','pcm_s24le',str(WORK/'mix.wav'))
    return levels,cues


def assemble():
    inputs=[WORK/'cards-aa.mp4',*CLIPS,WORK/'tail.mp4',WORK/'mix.wav'];argv=[]
    for p in inputs:argv+=['-i',str(p)]
    filters=[]
    for i,(a,b) in enumerate(SHOTS,1):
        # Tiniest edge dip softens hard black cuts without shortening the shot.
        fade=f',fade=t=in:d=0.15,fade=t=out:st={b-a-.18}:d=0.18'
        filters.append(f'[{i}:v]fps=30,scale=1280:720,setsar=1,tpad=stop_mode=clone:stop_duration=1,trim=duration={b-a},setpts=PTS-STARTPTS{fade}[s{i}]')
    for j,(a,b,*_) in enumerate(CARDS):
        filters.append(f'[0:v]trim=start_frame={round(a*FPS)}:end_frame={round(b*FPS)},setpts=PTS-STARTPTS[c{j}]')
    filters.append('[s1][c0][s2][c1][s3][c2][s4][c3][c4][5:v]concat=n=10:v=1:a=0[v]')
    target=OUT/'VoxWave-opening-v08-720p.mp4'
    run('-y',*argv,'-filter_complex',';'.join(filters),'-map','[v]','-map','6:a','-c:v','libx264','-crf','15',
        '-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart',str(target))
    return target


def main():
    levels,cues=make_sound();print('Mix prepared',flush=True)
    digest=render_graphics();print('Graphics and logo rendered',flush=True)
    target=assemble()
    report={'output':str(target),'duration':END,'resolution':'1280x720','fps':30,'audio':'48 kHz stereo',
            'phone_start':5.8,'ring_end':3.9,'phone_end':52.55,'question_start':QUESTION,'logo_tail_start':TAIL,
            'narration':cues,'ambience':levels,'card_wave_aa':4,'logo_aa':4,'envelope_attack':.085,
            'envelope_release':.24,'logo_extra_inertia':False,'canonical_logo_sha256':digest,
            'dialogue_regenerated':False,'api_calls':0,'text_changed':False}
    (WORK/'edit-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
