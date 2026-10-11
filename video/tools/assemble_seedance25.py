"""Local review reel and v06 integration; keep dialogue and logo timing intact."""
import subprocess
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]/'renders'
MEDIA=OUT/'seedance25'


def run(*args):
    subprocess.run(['ffmpeg','-hide_banner','-v','error','-y',*map(str,args)],check=True)


def main():
    durations=[6,5,5,5]
    clips=[MEDIA/f'm0{i}'/f'm0{i}-seedance25-v01.mp4' for i in range(1,5)]
    inputs=[]
    for clip in clips:inputs+=['-i',clip]
    filters=[]
    for i,duration in enumerate(durations):
        filters.append(f'[{i}:v]fps=30,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,trim=duration={duration},setpts=PTS-STARTPTS[v{i}]')
        gain_db=(8,10,15,6)[i]
        filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={duration},asetpts=PTS-STARTPTS,volume={gain_db}dB,afade=t=in:d=0.1,afade=t=out:st={duration-.15}:d=0.15[a{i}]')
    filters.append(''.join(f'[v{i}][a{i}]' for i in range(4))+'concat=n=4:v=1:a=1[v][a]')
    run(*inputs,'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]',
        '-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',MEDIA/'four-shots-review-v01.mp4')

    # Frame-accurate replacement of just the four placeholder shots.
    base=OUT/'opening-animatic-v05-restored.mp4'
    filters=[]
    for i,duration in enumerate(durations,1):
        filters.append(f'[{i}:v]fps=30,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,trim=duration={duration},setpts=PTS-STARTPTS[s{i}]')
    for j,(a,b) in enumerate(((6,11),(16,27),(32,37),(42,69))):
        filters.append(f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[c{j}]')
    filters.append('[s1][c0][s2][c1][s3][c2][s4][c3]concat=n=8:v=1:a=0[v]')
    for i,(start,duration,gain_db) in enumerate(zip((0,11,27,37),durations,(3,7,12,3)),1):
        filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={duration},asetpts=PTS-STARTPTS,volume={gain_db}dB,afade=t=in:d=0.15,afade=t=out:st={duration-.25}:d=0.25,adelay={start*1000}|{start*1000}[a{i}]')
    filters.append('[0:a][a1][a2][a3][a4]amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.95:level=0:latency=1[a]')
    run('-i',base,*inputs,'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]',
        '-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac',
        '-b:a','192k','-movflags','+faststart',OUT/'opening-v06-seedance25-ambience.mp4')
    print('Review reel and 69-second v06 integration complete.',flush=True)


if __name__=='__main__':main()
