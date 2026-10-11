"""Restore the selected 50 s conversation to v04, leaving its closing unchanged.
No API calls. v05 is a review baseline, not an approved final logo or performance.
"""
import array
import json
from render_brand_transition import OUT, RATE, decode, save_wav, run


def main():
    mix=decode(OUT/'opening-animatic-v04-soft.wav')
    shortened=decode(OUT/'opening-dialogue-v03-phone.wav')
    original=decode(OUT/'opening-dialogue-v02-phone-50s.wav')
    restored=array.array('h',mix)
    for i in range(len(original)):
        j=i-3*RATE
        removed=shortened[j]*.27 if 0<=j<len(shortened) else 0
        restored[i]=round(mix[i]-removed+original[i]*.27)
    assert restored[50*RATE:]==mix[50*RATE:]
    save_wav(OUT/'opening-animatic-v05-restored.wav',restored)
    visual=OUT/'opening-animatic-v05-restored-visual.mp4'
    run('-y','-i',str(OUT/'opening-animatic-v02-A-body-preserved.mp4'),
        '-i',str(OUT/'opening-animatic-v04-tail.mp4'),'-filter_complex',
        '[0:v]trim=end_frame=1680,setpts=PTS-STARTPTS[b];[b][1:v]concat=n=2:v=1:a=0[v]',
        '-map','[v]','-an','-c:v','libx264','-crf','18','-preset','fast',str(visual))
    run('-y','-i',str(visual),'-i',str(OUT/'opening-animatic-v05-restored.wav'),
        '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(OUT/'opening-animatic-v05-restored.mp4'))
    meta=json.loads((OUT/'opening-dialogue-v02-edit.json').read_text())
    request=json.loads((OUT.parent/'script/opening-dialogue-v02.request.json').read_text())
    lines=['# Conversation correction cues — restored v02', '',
        'No performances replaced yet. Owner to identify specific delivery corrections.', '']
    for cue,item in zip(meta['cues'],request['inputs']):
        lines.append(f"- {cue['start']:.2f}–{cue['end']:.2f} s: {item['text']}")
    (OUT.parent/'editing/dialogue-correction-cues.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Restored 11 turns; last segment ends',meta['cues'][-1]['end'],
          '; closing audio unchanged from 50 s onward.')


if __name__=='__main__': main()
