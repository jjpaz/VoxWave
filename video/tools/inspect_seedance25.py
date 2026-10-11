"""Local technical checks and contact sheets for generated Seedance clips."""
import json
import argparse
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parents[1]/'renders/seedance25'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phone-v02',action='store_true')
    args=parser.parse_args()
    root=OUT.parent/'seedance25-phone-v02' if args.phone_v02 else OUT
    version='v02' if args.phone_v02 else 'v01'
    for sid in (('m01',) if args.phone_v02 else ('m01','m02','m03','m04')):
        folder=root/sid;clip=folder/(sid+'-seedance25-'+version+'.mp4')
        if not clip.exists(): continue
        data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
            '-show_format','-of','json',str(clip)]))
        duration=float(data['format']['duration'])
        assert any(s['codec_type']=='audio' for s in data['streams']), 'Missing ambience track'
        assert duration>=(5.9 if sid=='m01' else 4.9)
        subprocess.run(['ffmpeg','-v','error','-i',str(clip),'-f','null','-'],check=True)
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vn','-c:a','pcm_s16le',
            str(folder/(sid+'-ambience.wav'))],check=True)
        times=[i*min(duration-.1,7.8 if args.phone_v02 else (5.8 if sid=='m01' else 4.8))/8 for i in range(9)]
        sheet=Image.new('RGB',(960,600),'#e5e5e5');draw=ImageDraw.Draw(sheet)
        for i,t in enumerate(times):
            frame=folder/f'frame-{i}.png'
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(clip),
                '-frames:v','1',str(frame)],check=True)
            with Image.open(frame) as im:sheet.paste(im.resize((320,180)),((i%3)*320,(i//3)*200))
            draw.text(((i%3)*320+8,(i//3)*200+183),f'{sid} {t:.2f}s',fill='black')
        sheet.save(folder/'contact.jpg')
        (folder/'verification.json').write_text(json.dumps({'duration':duration,
            'streams':[{k:s.get(k) for k in ('codec_type','codec_name','width','height','r_frame_rate','sample_rate','channels')}
                       for s in data['streams']], 'decode':'passed','audio_extracted':True},indent=2))
        print(sid,'decode OK, audio present, duration',duration,flush=True)


if __name__=='__main__':main()
