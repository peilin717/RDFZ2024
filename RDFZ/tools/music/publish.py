"""Publish only hashed static audio; local preview also exposes continuous-loop renders."""
import json,html,os
from pathlib import Path
from notation import ROOT
from render import WORK

def publish():
 catalog=json.loads((ROOT/'music/cues.json').read_text());manifest={'schema':1,'cues':{}};cards=[];keep=set()
 preview=WORK/'preview.html'
 link=WORK/'web'
 if not link.exists():link.symlink_to(ROOT/'assets/music',target_is_directory=True)
 for cue in catalog['bgm']+catalog['stingers']:
  id=cue['id'];s=json.loads((ROOT/f'music/scores/{id}.json').read_text());r=json.loads((WORK/f'reports/{id}-production.json').read_text())
  for file in [r['web'],r['fallback']]:
   assert (ROOT/file).exists(),file;keep.add(Path(file).name)
  manifest['cues'][id]={'title':cue['title'],'ogg':r['web'],'mp3':r['fallback'],'frames':r['frames'],'sampleRate':r['sample_rate'],'loop':r['loop'],'duration':r['duration']}
  sections=''.join(f"<li><b>{html.escape(a['name'])}</b> — {html.escape(a['description'])}</li>" for a in s['sections'])
  scene=cue.get('scene',cue.get('trigger',''));themes=' / '.join(s['themes'])
  cards.append(f'''<article id="{id}"><h2>{html.escape(cue['title'])} <small>{id}</small></h2><p>{html.escape(scene)} · {html.escape(themes)} · {r['duration']:.1f}秒 · {r['measured']['input_i']} LUFS</p><label>网页版本 <audio controls preload="none" src="web/{Path(r['web']).name}"></audio></label><label>{'连续三轮' if r['loop'] else '完整尾音'} <audio controls preload="none" src="previews/{Path(r['preview']).name}"></audio></label><details><summary>段落与编排</summary><ol>{sections}</ol></details><a href="masters/{id}.wav">无损母带</a></article>''')
 (ROOT/'music-manifest.js').write_text('window.RDFZMusicManifest = '+json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+';\n')
 # Remove only obsolete generated cue hashes, never arbitrary user audio.
 ids={c['id'] for c in catalog['bgm']+catalog['stingers']}
 for p in (ROOT/'assets/music').iterdir():
  bits=p.name.split('.')
  if len(bits)==3 and bits[0] in ids and len(bits[1])==12 and p.suffix in ('.ogg','.mp3') and p.name not in keep:p.unlink()
 preview.write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>回声与晨光 — RDFZ 原声</title><style>body{margin:32px auto;padding:0 20px;max-width:920px;background:#181b20;color:#eee7da;font:16px/1.6 system-ui}h1,h2{color:#e5c783}small{font-size:13px;color:#afa99e}article{padding:22px 0;border-bottom:1px solid #45413a}label{display:inline-flex;flex-direction:column;margin:8px 20px 8px 0}audio{max-width:100%}a{color:#b4d3ed}summary{cursor:pointer}li{margin:8px 0}</style><h1>回声与晨光</h1><p>RDFZ 2024 原创配乐 · 19首BGM / 6段短音乐。谱面、渲染、混音均本地完成。<strong>未进行主观听觉验证。</strong>此页供交付后浏览，不要求中间审批。</p><p>钢琴：Alexander Holm / Salamander Grand Piano，CC BY 3.0；Roberto / FreePats SF2转换。其他音色：S. Christian Collins / GeneralUser GS，按随附许可制作录音。转换版未包含所有SFZ踏板与释放噪声。</p>'''+''.join(cards)+'''<script>document.addEventListener('play',e=>{if(e.target.tagName==='AUDIO')document.querySelectorAll('audio').forEach(a=>{if(a!==e.target)a.pause()})},true)</script></html>''')
 (ROOT/'music/reports').mkdir(exist_ok=True)
 summary=[{'id':r['id'],'revision':r['revision'],'duration':r['duration'],'frames':r['frames'],'lufs':float(r['measured']['input_i']),'true_peak':float(r['measured']['input_tp']),'stems':len(r['stems']),'audition':r['audition']} for r in [json.loads((WORK/f"reports/{c['id']}-production.json").read_text()) for c in catalog['bgm']+catalog['stingers']]]
 (ROOT/'music/reports/production-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print('Published',len(manifest['cues']),'cues; local preview:',preview)
 return manifest
if __name__=='__main__':publish()
