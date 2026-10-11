"""Local phone revision: explicit answer/call cues, original complete dialogue.

No APIs. Leaves earlier exports intact. Shift all later visuals and audio equally
so existing card waveforms and the unchanged closing remain synchronized.
"""
import argparse
import array
import json
import math
from render_brand_transition import OUT, RATE, decode, save_wav, run


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--answer',type=float,required=True)
    parser.add_argument('--call-start',type=float,required=True)
    args=parser.parse_args()
    delta=args.call_start-3
    first_duration=6+delta
    assert 0<args.answer<args.call_start and first_duration>=8
    clip=OUT/'seedance25-phone-v02/m01/m01-seedance25-v02.mp4'
    source=decode(OUT/'opening-animatic-v05-restored.wav')
    original=decode(OUT/'opening-dialogue-v02-phone-50s.wav')
    # The original ring is entirely within the first 3 seconds. Retain its quiet
    # underlying score, subtracting only the deterministic old ringtone.
    intro=array.array('h')
    for i in range(round(args.call_start*RATE)):
        old_index=min(i,3*RATE-1)
        t=old_index/RATE
        old_ring=0
        if .2<t<.75 or 1.1<t<1.65:
            u=t-.2 if t<.75 else t-1.1
            old_ring=1500*min(1,u/.02,(.55-u)/.03)*math.sin(2*math.pi*440*t)
        # Beyond the retained intro use a very quiet matching musical bed.
        value=source[old_index]-old_ring if i<3*RATE else sum(
            a*math.sin(2*math.pi*f*i/RATE) for f,a in ((146.8324,36),(220,26),(329.6276,16),(440,8)))
        intro.append(round(value))
    mix=intro+source[3*RATE:]
    # Soft, simple feature-phone alert; gated exactly at the answer gesture.
    ringtone=array.array('h',[0])*len(mix)
    for i in range(round(.2*RATE),round(args.answer*RATE)):
        t=i/RATE
        phase=(t-.2)%1.15
        if phase<.72:
            gate=min(1,phase/.015,(.72-phase)/.035,(args.answer-t)/.015)
            note=(784,988,880)[min(2,int(phase/.24))]
            value=1800*gate*(math.sin(2*math.pi*note*t)+.18*math.sin(4*math.pi*note*t))
            ringtone[i]=round(value)
            mix[i]+=ringtone[i]
    assert not any(ringtone[round(args.answer*RATE):])
    assert len(mix)==len(source)+round(delta*RATE)
    save_wav(OUT/'opening-v07-core.wav',mix)
    save_wav(OUT/'seedance25-phone-v02/m01/ringtone-synced.wav',ringtone[:round(first_duration*RATE)])
    durations=[first_duration,5,5,5]
    clips=[clip]+[OUT/f'seedance25/m0{i}/m0{i}-seedance25-v01.mp4' for i in (2,3,4)]
    inputs=['-i',OUT/'opening-animatic-v05-restored.mp4']
    for path in clips: inputs+=['-i',path]
    inputs+=['-i',OUT/'opening-v07-core.wav']
    filters=[]
    for i,duration in enumerate(durations,1):
        filters.append(f'[{i}:v]fps=30,scale=1280:720,setsar=1,tpad=stop_mode=clone:stop_duration=4,trim=duration={duration},setpts=PTS-STARTPTS[s{i}]')
    for j,(a,b) in enumerate(((6,11),(16,27),(32,37),(42,69))):
        filters.append(f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[c{j}]')
    filters.append('[s1][c0][s2][c1][s3][c2][s4][c3]concat=n=8:v=1:a=0[v]')
    # New M01 kept at -6 dB; other environments 10 dB lower than v06.
    gains=(-6,-3,2,-7)
    for i,(start,duration,gain) in enumerate(zip((0,11+delta,27+delta,37+delta),durations,gains),1):
        filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration={duration},asetpts=PTS-STARTPTS,volume={gain}dB,afade=t=in:d=0.1,afade=t=out:st={duration-.25}:d=0.25,adelay={round(start*1000)}|{round(start*1000)}[a{i}]')
    filters.append('[5:a][a1][a2][a3][a4]amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.95:level=0:latency=1[a]')
    target=OUT/'opening-v07-phone-corrected.mp4'
    run('-y',*map(str,inputs),'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]',
        '-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(target))
    run('-y','-i',str(target),'-t',str(first_duration),'-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'m01-phone-v02-synced-720p.mp4'))
    meta=json.loads((OUT/'opening-dialogue-v02-edit.json').read_text())
    cues=[{**c,'start':c['start']+delta,'end':c['end']+delta} for c in meta['cues']]
    assert len(cues)==11 and cues[-1]['end']<50+delta
    report={'resolution':'1280x720','duration':69+delta,'answer':args.answer,
        'call_start':args.call_start,'time_shift':delta,'first_shot_duration':first_duration,
        'dialogue_cues':cues,'question_start':50+delta,'logo_tail_start':56+delta,
        'source_ambient_gain_db':gains,'m02_m04_change_vs_v06_db':-10,
        'voice_regenerated':False,'closing_design_changed':False}
    (OUT/'opening-v07-timing.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
