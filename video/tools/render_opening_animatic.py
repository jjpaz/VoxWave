"""Render the 50-second opening animatic locally with Pillow and FFmpeg.

No external calls, stock footage, or generated clinical signals. The four
illustrated shot studies are temporary placeholders. All waveform amplitudes
come from the final synthetic phone audio; the closing animation is the
owner's supplied reference, trimmed to its final five seconds.
"""
import array
import json
import math
import os
from pathlib import Path
import subprocess
import wave
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders'
W, H, FPS = 1280, 720, 30
ORANGE = '#FE653C'
WHITE = '#F4F8FA'
FONT = Path('C:/Windows/Fonts')


def font(size, bold=False):
    key = 'VOXWAVE_FONT_BOLD' if bold else 'VOXWAVE_FONT_REGULAR'
    selected = Path(os.environ.get(key, str(FONT / ('segoeuib.ttf' if bold else 'segoeui.ttf'))))
    if not selected.is_file():
        raise FileNotFoundError(f'Set {key} to a licensed font file; see video/handoff/README.md')
    return ImageFont.truetype(str(selected), size)


def run(*args):
    return subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', *args], check=True)


def center(draw, text, y, size, bold=False, fill=WHITE):
    f = font(size, bold)
    width = draw.textlength(text, font=f)
    assert width < W - 130, f'Text overflows: {text}'
    draw.text(((W-width)/2, y), text, font=f, fill=fill)


def card(lines, source):
    image = Image.new('RGB', (W,H), 'black')
    draw = ImageDraw.Draw(image)
    total = sum(size+17 for text,size,bold in lines)
    y = 307-total/2
    for text, size, bold in lines:
        center(draw, text, y, size, bold)
        y += size+17
    if source:
        for index, text in enumerate(source):
            center(draw, text, 637+index*23, 16, fill='#90979C')
    return image


def placeholder(kind, title, detail):
    image = Image.new('RGB', (W,H), '#142027')
    d = ImageDraw.Draw(image)
    dark, mid, light = '#1E3039', '#49606B', '#9CAFB5'
    # Simple storyboard shapes, deliberately distinct from finished footage.
    if kind == 1:
        d.polygon([(0,400),(1280,295),(1280,720),(0,720)], fill='#303A3D')
        for y in range(450,720,60):
            d.line([(0,y),(1280,y-100)], fill='#41494A', width=2)
        d.rounded_rectangle((565,210,730,545),24,fill='#101C24',outline=light,width=3)
        d.rounded_rectangle((589,250,706,344),5,fill='#6B7F7E')
        d.line((610,291,684,291),fill='#354A4D',width=3)
        for r in range(4):
            for c in range(3):
                x,y=587+c*40,375+r*34
                d.rounded_rectangle((x,y,x+29,y+22),5,outline=mid,width=2)
        d.polygon([(0,380),(258,363),(445,300),(527,310),(585,345),(572,386),
                   (491,371),(426,410),(290,445),(0,485)],fill='#7D8582',outline=light,width=2)
        d.polygon([(0,369),(221,355),(251,453),(0,488)],fill=dark,outline=mid)
        d.ellipse((952,370,1092,422),fill=dark,outline=mid,width=2)
    elif kind == 2:
        d.rectangle((190,120,1100,620),fill='#34464C')
        d.rectangle((770,175,1035,414),fill='#899D9F',outline=light,width=4)
        d.line((902,175,902,414),fill=dark,width=8)
        d.line((770,292,1035,292),fill=dark,width=8)
        d.polygon([(755,164),(795,164),(778,455),(735,470)],fill='#6B7F81')
        d.polygon([(0,0),(205,0),(205,720),(0,720)],fill='#0B141A')
        d.rectangle((1080,0,1280,720),fill='#0B141A')
        d.polygon([(205,620),(1080,620),(1220,720),(68,720)],fill='#29353A')
        d.rounded_rectangle((420,340,677,513),35,fill='#52656A',outline=light,width=2)
        d.rounded_rectangle((396,454,700,571),23,fill=dark,outline=mid,width=3)
        d.rectangle((412,567,431,623),fill=mid)
        d.rectangle((665,567,684,623),fill=mid)
        d.polygon([(580,368),(643,365),(677,541),(611,552)],fill='#82918F')
        d.ellipse((721,455,890,487),fill='#665F53',outline=light,width=2)
        d.line((741,480,741,604),fill=mid,width=7)
        d.line((874,480,874,604),fill=mid,width=7)
        d.rounded_rectangle((787,420,826,461),5,fill='#BDCAC6')
        d.arc((814,427,844,453),270,90,fill='#BDCAC6',width=4)
    elif kind == 3:
        d.rectangle((0,140,W,363),fill='#75878C')
        d.rectangle((0,363,W,720),fill='#344742')
        d.polygon([(620,357),(654,357),(1035,720),(265,720)],fill='#5A6260')
        d.line([(620,357),(265,720)],fill='#A0A79A',width=3)
        d.line([(654,357),(1035,720)],fill='#A0A79A',width=3)
        for x,y,height in [(125,372,192),(256,360,143),(1075,380,219),(948,360,157)]:
            d.line((x,y,x+9,y-height),fill='#AEBBB8',width=8)
            for offset in (45,75,110):
                d.line((x+5,y-offset,x-29,y-offset-36),fill=mid,width=3)
                d.line((x+5,y-offset,x+39,y-offset-45),fill=mid,width=3)
        d.line((0,395,510,380),fill=mid,width=2)
        d.line((760,388,1280,410),fill=mid,width=2)
    else:
        d.polygon([(0,100),(510,250),(510,466),(0,720)],fill='#40545D')
        d.polygon([(1280,100),(770,250),(770,466),(1280,720)],fill='#344952')
        d.polygon([(0,720),(510,466),(770,466),(1280,720)],fill='#243740')
        d.rectangle((510,250,770,466),fill='#72848B')
        d.rectangle((567,281,711,465),fill='#3E545F',outline=light,width=3)
        d.ellipse((688,371,695,378),fill=light)
        for x,y,s in [(173,412,1.0),(335,379,.72),(442,355,.49)]:
            d.rounded_rectangle((x,y,x+112*s,y+87*s),int(9*s),fill=dark,outline=light,width=2)
            d.polygon([(x,y+90*s),(x+112*s,y+90*s),(x+131*s,y+123*s),(x-16*s,y+123*s)],fill=mid)
            for a in (0,108):
                d.line((x+a*s,y+121*s,x+a*s,y+185*s),fill=light,width=3)
        for i in range(3):
            y=172+i*29
            d.line((580+i*17,y,710-i*17,y),fill=light,width=4)
    # Letterbox and explicit edit annotations, removed for final footage.
    d.rectangle((0,0,W,111),fill='#091217')
    d.rectangle((0,623,W,H),fill='#091217')
    d.text((64,27),f'M0{kind}  /  {title}',font=font(25,True),fill=WHITE)
    d.text((64,68),'SHOT STUDY · PLACEHOLDER',font=font(15),fill=ORANGE)
    d.text((64,652),detail,font=font(20),fill='#AFBEC5')
    return image


def main():
    cards = [
        (5,10,card([('More than 10 million',57,True),('people worldwide live with',43,False),
                    ('Parkinson’s disease',47,False)],["Parkinson’s Foundation · Global estimate"])),
        (13,23,card([('Parkinson’s is the fastest-growing',43,True),
                     ('neurological condition in the world,',43,False),
                     ('with global cases projected to reach',43,False),
                     ('over 25 million by 2050.',49,True)],
                    ['BMJ, 2025 · Projection based on GBD 2021',
                     'Growth ranking: prevalence and disability, GBD 2015'])),
        (26,31,card([('Symptoms can appear',49,False),('long before',57,True),
                     ('they are recognised.',49,False)],["Parkinson’s UK · Diagnosis information"])),
        (34,39,card([('Seeing a specialist can mean',47,False),('months of waiting',57,True)],
                    ['Lithuania specialist-care survey · LRT / Baltijos tyrimai, 2025'])),
        (39,44,card([('What if the answer was',50,False),('here all along?',59,True)],[])),
    ]
    shots = [(0,5,placeholder(1,'THE CALL','Close-up · A hand answers a button mobile · No face')),
             (10,13,placeholder(2,'AT HOME','Hallway, window, armchair, blanket and a single cup')),
             (23,26,placeholder(3,'THE DISTANCE','An empty rural Baltic road · Locked wide shot')),
             (31,34,placeholder(4,'THE WAIT','Waiting chairs and a closed consultation-room door'))]
    assert sum(b-a for a,b,_ in cards+shots)+1+5 == 50
    # Derive a compact amplitude envelope directly from decoded phone speech.
    with wave.open(str(OUT/'opening-dialogue-v02-phone-50s.wav'),'rb') as source:
        assert source.getframerate()==44100 and source.getnchannels()==1
        pcm=array.array('h',source.readframes(source.getnframes()))
    step=441  # ten-millisecond RMS windows
    levels=[math.sqrt(sum(x*x for x in pcm[i:i+step])/step)/32768 for i in range(0,len(pcm),step)]
    scale=sorted(levels)[int(.98*len(levels))]
    assert scale>0 and max(levels[:290])==0
    def wave_frame(image,t):
        d=ImageDraw.Draw(image)
        progress=max(0,min(1,(t-44)/.8))
        progress=progress*progress*(3-2*progress)
        baseline=548+(360-548)*progress
        width=640
        # A mirrored recent-history envelope. No fake minimum activity in silence.
        points=[]
        for j in range(161):
            u=j/160
            at=t-.16+u*.16
            index=max(0,min(len(levels)-1,int(at*100)))
            amplitude=min(1.3,levels[index]/scale)*math.sin(math.pi*u)**2
            carrier=math.sin(u*math.pi*6+t*2.3)
            height=amplitude*38*carrier
            height*=1-progress*.75
            points.append((320+width*u,baseline+height))
        d.line(points,fill=ORANGE,width=3,joint='curve')
        d.line([(x,2*baseline-y) for x,y in points],fill=ORANGE,width=2,joint='curve')
        return image
    visual=OUT/'opening-animatic-v01-body.mp4'
    cmd=['ffmpeg','-hide_banner','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264',
         '-preset','fast','-crf','19','-pix_fmt','yuv420p',str(visual)]
    snapshots={60,210,345,510,735,855,975,1095,1245,1335}
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
        for frame in range(45*FPS):
            t=frame/FPS
            image=Image.new('RGB',(W,H),'black')
            for a,b,base in cards+shots:
                if a<=t<b:
                    image=base.copy()
                    if (a,b,base) in cards:
                        opacity=min(1,(t-a)/.23,(b-t)/.18)
                        image=Image.blend(Image.new('RGB',(W,H),'black'),image,max(0,opacity))
                    break
            if any(a<=t<b for a,b,_ in cards) or 44<=t<45:
                wave_frame(image,t)
            if frame in snapshots:
                image.save(OUT/f'animatic-frame-{frame:04d}.jpg',quality=92)
            process.stdin.write(image.tobytes())
            if frame%300==0:
                print(f'Rendered {frame}/{45*FPS} frames',flush=True)
        process.stdin.close()
        assert process.wait()==0
    ref=ROOT/'references/motion/voxwave_logo_reveal DEFINITIVO.mp4'
    # Owner reference has 286 frames. Use final 150 frames without speeding it up.
    run('-y','-i',str(ref),'-vf',
        f'trim=start_frame=136:end_frame=286,setpts=PTS-STARTPTS,scale={W}:{H},fps={FPS}',
        '-an','-c:v','libx264','-crf','19','-preset','fast','-pix_fmt','yuv420p',
        str(OUT/'opening-animatic-v01-logo.mp4'))
    run('-y','-i',str(visual),'-i',str(OUT/'opening-animatic-v01-logo.mp4'),
        '-i',str(OUT/'opening-dialogue-v02-preview-50s.wav'),
        '-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a]volume=0.6[a]',
        '-map','[v]','-map','[a]','-c:v','libx264','-crf','19','-preset','fast',
        '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',
        str(OUT/'opening-animatic-v01.mp4'))
    print('Created opening-animatic-v01.mp4',flush=True)


if __name__=='__main__':
    main()
