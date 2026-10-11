"""Check the exported opening, cue ordering, silence response and audio levels."""
import array
import json
import math
import subprocess
from PIL import Image, ImageDraw
import finalize_opening_v08 as v


def main():
    clip=v.OUT/'VoxWave-opening-v08-720p.mp4'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(clip)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert (video['width'],video['height'],video['r_frame_rate'])==(1280,720,'30/1')
    assert audio['sample_rate']=='48000' and audio['channels']==2
    assert int(video['nb_frames'])==round(v.END*30)
    assert abs(float(probe['format']['duration'])-v.END)<.06
    subprocess.run(['ffmpeg','-v','error','-i',str(clip),'-f','null','-'],check=True)
    meta=json.loads((v.WORK/'edit-report.json').read_text())
    assert meta['ring_end']<meta['phone_start']<meta['phone_end']<meta['question_start']<meta['logo_tail_start']<meta['narration'][0]['start']
    assert meta['narration'][0]['end']<meta['narration'][1]['start']<meta['narration'][1]['end']<v.END-2
    # Every original dialogue turn remains inside the call, with the same shift.
    original=json.loads((v.OUT/'opening-dialogue-v02-edit.json').read_text())['cues']
    assert len(original)==11 and abs(original[-1]['end']+2.8-meta['phone_end'])<.001
    call=v.base.decode(v.OUT/'opening-dialogue-v02-phone-50s.wav')
    call.extend(array.array('h',[0])*round(10*v.RATE))
    levels,dt=v.envelope(call)
    assert max(levels[:int(2.9/dt)])==0
    assert v.level_at(levels,dt,54)==0
    narrator=v.base.decode(v.OUT/'brand-narration-v02-timed.wav')
    levels,dt=v.envelope(narrator)
    assert v.level_at(levels,dt,57)==0
    assert v.level_at(levels,dt,57.9)>.01
    assert v.level_at(levels,dt,62)<.01, 'Narrator pause must not keep large fluctuations'
    assert v.level_at(levels,dt,68)==0
    # Inspect shots, all four complete cards, question, logo progression, final hold.
    times=[.7,2.5,4.5,5.8,10.5,16,22,32,37,42,47,53.8,59.5,61.5,63,65.8,67,70.8]
    sheet=Image.new('RGB',(4*320,5*204),'#202020');draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        p=v.WORK/f'qa-{t:.1f}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(clip),'-frames:v','1',str(p)],check=True)
        with Image.open(p) as im: sheet.paste(im.resize((320,180)),((i%4)*320,(i//4)*204))
        draw.text(((i%4)*320+8,(i//4)*204+184),f'{t:.1f} s',fill='white')
    sheet.save(v.WORK/'qa-contact.jpg',quality=95)
    result=subprocess.run(['ffmpeg','-hide_banner','-i',str(clip),'-af','loudnorm=I=-23:TP=-2:LRA=9:print_format=json','-vn','-f','null','-'],capture_output=True,text=True,check=True)
    stats=json.loads(result.stderr[result.stderr.rfind('{'):result.stderr.rfind('}')+1])
    assert float(stats['input_tp'])<-2
    report={'decode':'passed','resolution':'1280x720','duration':probe['format']['duration'],
            'frames':video['nb_frames'],'audio_sample_rate':audio['sample_rate'],'audio_channels':audio['channels'],
            'cue_order':'passed','original_dialogue_turns':11,'silence_waveform':'passed',
            'integrated_lufs':stats['input_i'],'true_peak_dbtp':stats['input_tp'],'loudness_range_lu':stats['input_lra'],
            'review_scope':'Frames, source script/cues, measured loudness and complete decoding; artistic listening remains subjective.'}
    (v.WORK/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
