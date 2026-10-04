"""Authored themes and three complete representative compositions.
This file is a score source, not a stochastic song generator.
"""
import json
from notation import ROOT, notes, bars, transform, part as P, section as S, chord_part as H, percussion as D, score
CUES={x['id']:x for x in json.loads((ROOT/'music/cues.json').read_text())['bgm']}
CAMPUS='D5:1 A4:.5 C5:.5 F5:1 E5:.5 r:.5 | D5:1.5 C5:.5 A4:1 r:1 | Bb4:.5 D5:.5 G5:1 F5:.5 E5:.5 D5:1 | C5:2 A4:1 r:1 | F5:.75 G5:.25 A5:1 G5:.5 F5:.5 E5:1 | D5:1 F5:.5 E5:.5 C5:1 r:1 | Bb4:1 A4:.5 G4:.5 A4:1 C5:.5 E5:.5 | D5:2.5 A4:.5 r:1'
INTRUSION='E5:.5 F5:.5 r:.5 Bb4:.5 E5:1 r:1 | r:.5 F5:.5 E5:1 B4:.5 r:1.5 | E5:.5 r:1 Bb4:.5 A4:.5 F5:.5 r:1 | D#5:1 E5:.5 r:2.5 | Bb4:.5 E5:.5 F5:1 r:.5 B4:.5 r:1 | G5:.5 F5:.5 r:1 E5:.5 D#5:.5 r:1 | A4:1 Bb4:.5 r:.5 F5:.5 E5:.5 r:1 | F5:.5 E5:1.5 r:2'
RESOLVE='A4:.5 D5:1.5 F5:.5 E5:.5 D5:.5 r:.5 | C5:.75 D5:.25 A4:1 C5:.5 D5:1 r:.5 | F5:.5 A5:1 G5:.5 F5:.5 E5:.5 D5:.5 r:.5 | E5:1 A4:1 C#5:.5 E5:1 r:.5 | D5:.5 F5:.5 A5:1 C6:.5 A5:.5 G5:1 | F5:.75 E5:.25 D5:1 C5:.5 A4:1 r:.5 | Bb4:.5 D5:1 F5:.5 E5:.5 C#5:.5 A4:.5 r:.5 | D5:1.5 E5:.5 A4:1 r:1'
THEMES={'campus':('校园与伙伴',CAMPUS,'五度回望、短短长回答；D小调暖色'), 'intrusion':('AI侵蚀',INTRUSION,'半音触碰、3+3+2破碎脉冲与缺席的落点'), 'resolve':('抵抗与希望',RESOLVE,'上行四度、附点与切分、拱形高点')}
for id,(name,text,identity) in THEMES.items():
 (ROOT/f'music/themes/{id}.json').write_text(json.dumps({'id':id,'name':name,'meter':[4,4],'bars':8,'identity':identity,'notation':text,'notes':notes(text,velocity=75),'motif_bars':[1,2],'phrase_ends':[4,8]},ensure_ascii=False,indent=2)+'\n')
REST=' | '.join(['r:4']*8)
HOME_H1=['F3 A3 D4 E4','E3 G3 C4 D4','D3 G3 Bb3 D4','E3 A3 C4 E4','F3 A3 C4 F4','F3 A3 D4 F4','D3 G3 Bb3 D4','E3 G3 A3 C#4']
HOME_H2=['A3 C4 F4 G4','G3 C4 E4 G4','A3 C4 D4 F4','G3 Bb3 D4 F4','G3 C4 E4 G4','A3 C4 F4 A4','G3 Bb3 D4 E4','G3 A3 C#4 E4']
HOME_BASS='D3:1 A2:.5 C3:.5 D3:1 E3:.5 r:.5 | C3:1 G2:1 B2:.5 C3:.5 r:1 | Bb2:1 F3:.5 E3:.5 D3:1 r:1 | A2:1 E3:1 G3:.5 E3:.5 r:1 | F2:1 C3:.5 E3:.5 F3:1 E3:1 | D3:1 A2:.5 C3:.5 F3:1 E3:.5 r:.5 | G2:1 D3:1 Bb2:.5 C3:.5 D3:.5 r:.5 | A2:1 E3:1 G3:.5 E3:.5 C#3:.5 r:.5'
HOME_BB='F2:1 C3:1 A2:.5 C3:.5 E3:.5 r:.5 | E3:1 C3:.5 B2:.5 G2:1 C3:1 | D3:1 A2:1 C3:.5 D3:.5 E3:.5 r:.5 | Bb2:1 F3:.5 D3:.5 Bb2:1 A2:1 | C3:1 G2:1 B2:.5 C3:.5 D3:.5 r:.5 | A2:1 C3:.5 E3:.5 F3:1 C3:1 | G2:1 D3:.5 F3:.5 E3:1 D3:1 | A2:1 E3:.5 G3:.5 C#3:1 r:1'
HOME_B='A5:1 G5:.5 E5:.5 F5:1 r:1 | G5:.5 E5:.5 D5:1 C5:.5 E5:.5 r:1 | F5:1 E5:.5 D5:.5 A4:1 C5:1 | D5:1 F5:.5 G5:.5 Bb5:1 A5:.5 r:.5 | G5:1.5 E5:.5 D5:.5 C5:.5 r:1 | F5:.5 A5:.5 C6:1 A5:1 G5:.5 r:.5 | F5:1 E5:1 D5:.5 C5:.5 Bb4:.5 r:.5 | A4:1 C#5:.5 E5:.5 G5:1 r:1'
HOME_C='r:1 A4:1 D5:.5 E5:.5 F5:1 | E5:1 C5:.5 A4:.5 G4:1 r:1 | Bb4:1 D5:1 F5:.5 E5:.5 r:1 | E5:1 C#5:1 A4:.5 G4:.5 r:1 | A4:.5 C5:.5 F5:1 G5:.5 A5:.5 r:1 | F5:1 D5:.5 C5:.5 A4:1 r:1 | G4:.5 Bb4:.5 D5:1 E5:1 C5:.5 r:.5 | A4:1 C#5:.5 E5:.5 A4:1 r:1'
HOME_REPLY='r:3 A4:.5 C5:.5 | r:2 G4:.5 A4:.5 C5:.5 r:.5 | r:3 Bb4:.5 A4:.5 | r:2 E4:1 r:1 | r:3 C5:.5 E5:.5 | r:2 A4:.5 G4:.5 F4:.5 r:.5 | r:3 D5:.5 C5:.5 | r:2 C#5:.5 A4:.5 r:1'

def home():
 return score(CUES['home'],[
 S('A · 窗边的点名','1–8 钢琴清楚陈述校园主题，吉他留拍，低音上行连接。',piano=P('piano',CAMPUS,71),nylon=P('nylon',H(HOME_H1,'breath'),48,role='harmony',gain=.65),bass=P('bass',HOME_BASS,51,role='bass',gain=.8)),
 S("A′ · 同伴回答",'9–16 长笛接过主题尾句，钢琴回应只在主句空隙；竖琴不持续琶音。',flute=P('flute',transform(CAMPUS,replacement={2:'G5:1 F5:.5 E5:.5 D5:1 Bb4:.5 r:.5',7:'D5:1 F5:1 E5:.5 D5:.5 r:1'}),64,gain=.65),piano=P('piano',HOME_REPLY,54,role='response'),nylon=P('nylon',H(HOME_H1,'dialogue'),49,role='harmony',gain=.65),bass=P('bass',transform(HOME_BASS,replacement={0:'F3:1 E3:.5 D3:.5 A2:1 C3:.5 r:.5',2:'D3:1 F3:.5 G3:.5 Bb2:1 A2:1',4:'A2:1 C3:1 F3:.5 G3:.5 E3:1',7:'C#3:1 E3:1 A2:.5 G2:.5 r:1'}),50,role='bass',gain=.8)),
 S('B · 走向中庭','17–24 转向F明亮区域，旋律长线越过原动机；低音不跟随主旋律。',piano=P('piano',HOME_B,73),strings=P('strings',H(HOME_H2,'held'),45,role='harmony',gain=.42),bass=P('bass',HOME_BB,54,role='bass',gain=.8)),
 S('C · 未说完的话','25–32 高潮后撤去弦乐，单簧管中音区逆向回应，拨弦切分。',clarinet=P('clarinet',HOME_C,62),nylon=P('nylon',H(HOME_H1,'offbeat'),50,role='harmony',gain=.65),bass=P('bass',transform(HOME_BASS,replacement={1:'C3:2 E3:.5 G3:.5 r:1',5:'D3:1 C3:1 A2:1 r:1'}),48,role='bass',gain=.8)),
 S('A″ · 记住彼此','33–40 钢琴回归但高点延长、尾句重写，弦乐仅两拍呼吸。',piano=P('piano',transform(CAMPUS,replacement={4:'A5:1.5 G5:.5 F5:1 E5:.5 r:.5',5:'D5:.5 F5:.5 A5:1 F5:1 r:1',7:'F5:1 E5:.5 D5:.5 C5:1 A4:.5 r:.5'}),74),strings=P('strings',H(HOME_H1,'breath'),43,role='harmony',gain=.42),bass=P('bass',HOME_BASS,52,role='bass',gain=.8)),
 S('回廊 · 再会的入口','41–48 校园动机缩短，属和声收束为下一轮弱起留空间。',flute=P('flute',transform(HOME_C,replacement={0:'r:2 D5:.5 E5:.5 F5:1',2:'Bb4:1 D5:.5 F5:.5 r:2',4:'A4:.5 C5:.5 F5:1 r:2',6:'G4:1 Bb4:.5 D5:.5 E5:.5 C5:.5 r:1',7:'C#5:1 E5:.5 G5:.5 A4:.5 r:1.5'}),59,gain=.65),piano=P('piano',HOME_REPLY,52,role='response'),nylon=P('nylon',H(HOME_H1,'breath'),46,role='harmony',gain=.65),bass=P('bass',HOME_BASS,47,role='bass',gain=.8))])

EXP_A='E5:.5 F5:.5 r:1 Bb4:1 r:1 | r:1 E5:.5 D#5:.5 E5:1 r:1 | G5:1 r:.5 F5:.5 E5:.5 Bb4:.5 r:1 | A4:1 E5:.5 r:2.5 | E5:.5 F5:.5 B4:1 r:2 | r:1.5 Bb4:.5 A4:1 G4:.5 r:.5 | F5:1 E5:.5 D5:.5 Bb4:1 r:1 | B4:.5 D#5:.5 E5:1 r:2'
EXP_B='G4:1 B4:.5 D5:.5 E5:1 r:1 | D5:1 G4:1 A4:.5 B4:.5 r:1 | C5:1 E5:.5 G5:.5 F#5:1 E5:.5 r:.5 | D5:1 B4:.5 A4:.5 G4:1 r:1 | A4:.5 C5:.5 E5:1 D5:1 r:1 | G4:1 B4:1 A4:.5 G4:.5 r:1 | F#4:1 A4:.5 C5:.5 B4:1 r:1 | D#5:.5 E5:.5 B4:1 r:2'
EXP_C='r:1 E4:.5 F4:.5 Bb4:1 r:1 | B4:1 F4:.5 E4:.5 r:2 | G4:.5 A4:.5 Bb4:1 r:.5 E5:.5 r:1 | F5:1 E5:1 r:2 | r:.5 E4:.5 Bb4:.5 E5:.5 F5:.5 r:1.5 | D#5:1 B4:.5 A4:.5 r:2 | F4:1 A4:.5 Bb4:.5 E5:1 r:1 | F5:.5 E5:.5 D#5:1 r:2'
EXP_H=['E3 G3 B3 F4','D#3 A3 B3 E4','E3 G3 C4 F#4','D3 G3 B3 E4','C3 G3 Bb3 E4','D3 F3 A3 Bb3','C3 F3 A3 E4','D#3 F#3 A3 B3']
EXP_HB=['G3 B3 D4 E4','G3 B3 D4 F#4','G3 C4 E4 G4','G3 B3 D4 F#4','A3 C4 E4 G4','G3 B3 D4 E4','F#3 A3 C4 E4','F#3 A3 B3 D#4']
EXP_LOW='E2:2 B2:.5 r:1.5 | D#3:1 B2:1 r:2 | C3:1 G2:1 B2:.5 r:1.5 | B2:2 A2:.5 G2:.5 r:1 | C3:1 G2:1 Bb2:1 r:1 | D3:1 A2:.5 C3:.5 r:2 | F2:1 C3:1 E3:.5 r:1.5 | B2:1 F#2:.5 A2:.5 D#3:1 r:1'
EXP_LOWB='G2:1 D3:1 B2:.5 r:1.5 | F#2:1 B2:1 D3:.5 r:1.5 | E3:1 C3:.5 B2:.5 G2:1 r:1 | D3:1 B2:1 A2:.5 r:1.5 | A2:1 E3:.5 G3:.5 C3:1 r:1 | B2:1 D3:1 G2:.5 r:1.5 | F#2:1 C3:1 A2:.5 r:1.5 | B2:1 A2:1 F#2:.5 D#3:.5 r:1'
EXP_REPLY='r:2 E4:.5 G4:.5 r:1 | r:3 B3:.5 r:.5 | r:2 C4:1 r:1 | r:3 G4:.5 F4:.5 | r:2 G4:.5 Bb4:.5 r:1 | r:2 F4:.5 E4:.5 D4:.5 r:.5 | r:3 C4:.5 r:.5 | r:2 D#4:.5 F#4:.5 r:1'
def basement():
 return score(CUES['basement'],[
 S('I · 门缝','1–8 电钢断句与低音之间存在空白；半音并不连续轰鸣。',electric=P('electric',EXP_A,58),cello=P('cello',H(EXP_H,'breath'),42,role='atmosphere',gain=.42),bass=P('bass',EXP_LOW,48,role='bass',gain=.75)),
 S('II · 回声有方向','9–16 单簧管把电钢碎片连成疑问；低音开始反向运动。',clarinet=P('clarinet',EXP_C,55),electric=P('electric',EXP_REPLY,48,role='response'),bass=P('bass',EXP_LOWB,45,role='bass',gain=.75)),
 S('III · 旧窗的日光','17–24 G区钢琴展开长句，出现真正的暖色对比，不只是换音色。',piano=P('piano',EXP_B,70,gain=1.18),nylon=P('nylon',H(EXP_HB,'dialogue'),44,role='harmony',gain=.6),bass=P('bass',EXP_LOWB,47,role='bass',gain=.75)),
 S('IV · 失去一个音','25–32 将原3+3+2片段拆为跨拍问答，钢琴缺席，木管留白。',clarinet=P('clarinet',transform(EXP_A,octave=-1,replacement={3:'r:2 B4:.5 A4:.5 r:1',6:'F5:.5 r:.5 E5:1 Bb4:.5 r:1.5'}),58),electric=P('electric',transform(EXP_REPLY,replacement={0:'r:3 E4:.5 F4:.5',2:'r:2.5 C4:.5 B3:.5 r:.5',4:'r:3 Bb3:.5 E4:.5',6:'r:2 F4:.5 E4:.5 r:1'}),46,role='response'),cello=P('cello',H(EXP_H,'held'),40,role='atmosphere',gain=.42)),
 S('V · 门仍未关','33–40 电钢回归改变落点，末两小节导向E，不制造静音洞。',electric=P('electric',transform(EXP_A,replacement={4:'B4:1 E5:.5 F5:.5 r:2',5:'r:1 A4:.5 Bb4:.5 E5:1 r:1',7:'F5:.5 E5:.5 D#5:1 B4:.5 r:1.5'}),57),nylon=P('nylon',H(EXP_H,'breath'),42,role='harmony',gain=.6),bass=P('bass',EXP_LOW,47,role='bass',gain=.75))])

BAT_H=['F3 A3 D4 F4','E3 A3 C4 E4','F3 Bb3 D4 F4','E3 A3 C#4 E4','F3 A3 C4 F4','F3 Bb3 D4 F4','E3 G3 Bb3 D4','E3 G3 A3 C#4']
BAT_HB=['G3 C4 E4 G4','F3 A3 C4 F4','F3 Bb3 D4 F4','G3 Bb3 D4 G4','G3 C4 E4 G4','F3 A3 D4 F4','F3 Bb3 D4 E4','E3 G3 A3 C#4']
BAT_BASS='D2:.75 A2:.25 D3:.5 r:.5 C3:.5 A2:.5 F2:.5 E2:.5 | A2:.75 E3:.25 C3:.5 r:.5 A2:.5 G2:.5 E2:1 | Bb2:.5 F3:.5 D3:.75 C3:.25 Bb2:.5 A2:.5 G2:.5 F2:.5 | A2:.75 E3:.25 G3:.5 r:.5 E3:.5 C#3:.5 A2:1 | F2:.5 C3:.5 F3:.75 E3:.25 C3:.5 A2:.5 G2:.5 A2:.5 | Bb2:.75 D3:.25 F3:.5 r:.5 D3:.5 Bb2:.5 A2:1 | G2:.5 D3:.5 F3:.75 E3:.25 D3:.5 Bb2:.5 A2:.5 G2:.5 | A2:.75 E3:.25 G3:.5 r:.5 C#3:.5 B2:.5 A2:.5 C#3:.5'
BAT_BB='C3:.75 G2:.25 B2:.5 C3:.5 E3:.5 r:.5 G2:1 | A2:.5 C3:.5 F3:1 E3:.5 C3:.5 A2:1 | Bb2:1 D3:.5 F3:.5 A3:.5 F3:.5 D3:.5 r:.5 | G2:.75 D3:.25 F3:.5 r:.5 Bb2:.5 A2:.5 G2:1 | E3:1 C3:.5 G2:.5 B2:.5 C3:.5 D3:.5 r:.5 | D3:.5 A2:.5 C3:1 F3:.5 E3:.5 D3:.5 r:.5 | Bb2:.75 F3:.25 D3:.5 r:.5 C3:.5 Bb2:.5 G2:1 | A2:.5 E3:.5 G3:.5 E3:.5 C#3:.5 B2:.5 A2:.5 r:.5'
BAT_B='G5:1 E5:.5 D5:.5 C5:1 r:1 | F5:.75 E5:.25 C5:1 A4:.5 C5:.5 D5:.5 r:.5 | D5:.5 F5:.5 Bb5:1 A5:.5 F5:.5 D5:1 | G5:1 F5:.5 D5:.5 Bb4:1 r:1 | E5:.5 G5:.5 C6:1 B5:.5 G5:.5 E5:.5 r:.5 | A5:1 F5:1 E5:.5 D5:.5 C5:.5 r:.5 | Bb4:.5 D5:1 G5:.5 F5:.5 E5:.5 D5:.5 r:.5 | C#5:1 E5:.5 G5:.5 A5:1 r:1'
BAT_C='r:.5 D5:.5 F5:.5 A5:.5 r:.5 G5:.5 F5:.5 E5:.5 | D5:1 A4:.5 r:.5 C5:.5 D5:.5 F5:1 | A5:.5 F5:.5 D5:1 Bb4:.5 D5:.5 F5:.5 r:.5 | E5:.5 C#5:.5 A4:1 G4:.5 A4:.5 C#5:1 | F5:1 A5:.5 C6:.5 A5:.5 G5:.5 F5:.5 r:.5 | D5:.5 F5:1 Bb5:.5 A5:.5 F5:.5 D5:1 | G5:.5 F5:.5 D5:1 E5:.5 F5:.5 G5:.5 r:.5 | E5:.5 C#5:.5 A4:.5 G4:.5 E5:1 r:1'
BAT_R='r:2 A4:.5 C5:.5 D5:.5 r:.5 | r:2 E4:.5 G4:.5 A4:1 | r:2 F4:.5 Bb4:.5 A4:.5 r:.5 | r:2 C#5:.5 A4:.5 G4:.5 r:.5 | r:2 C5:.5 E5:.5 F5:.5 r:.5 | r:2 D5:.5 F5:.5 Bb4:1 | r:2 Bb4:.5 A4:.5 G4:.5 r:.5 | r:2 C#5:.5 E5:.5 A4:.5 r:.5'
def battle():
 return score(CUES['battle'],[
 S('起势 · 留出第一步','1–8 尼龙弦切分与拨奏低音，木管陈述希望主题，鼓只定骨架。',clarinet=P('clarinet',RESOLVE,76),nylon=P('nylon',H(BAT_H,'offbeat'),62,role='harmony',gain=.8),ebass=P('ebass',BAT_BASS,66,role='bass',gain=.68),drums=P('drums',D('backbeat',8),60,role='rhythm',gain=.6)),
 S('A′ · 交错掩护','9–16 钢琴接棒，末句上行不完全终止；弦乐只接第二拍。',piano=P('piano',transform(RESOLVE,replacement={3:'E5:.5 A5:1 G5:.5 E5:.5 C#5:.5 A4:.5 r:.5',7:'D5:.5 F5:.5 E5:.5 C#5:.5 A4:1 r:1'}),80),strings=P('strings',H(BAT_H,'breath'),49,role='harmony',gain=.43),ebass=P('ebass',BAT_BASS,64,role='bass',gain=.75),drums=P('drums',D('drive',8),60,role='rhythm',gain=.6)),
 S('B · 看见出口','17–24 明亮C/F和声与长线旋律；减少鼓击给线条空间。',flute=P('flute',BAT_B,72,gain=.68),nylon=P('nylon',H(BAT_HB,'dialogue'),57,role='harmony',gain=.8),ebass=P('ebass',BAT_BB,63,role='bass',gain=.75),drums=P('drums',D('light',8),50,role='rhythm',gain=.6)),
 S('B′ · 回答不退让','25–32 单簧管低八度收拢B段，钢琴在休止处回应。',clarinet=P('clarinet',transform(BAT_B,octave=-1,replacement={4:'G5:.5 C6:1 B5:.5 G5:.5 E5:.5 D5:.5 r:.5'}),77),piano=P('piano',BAT_R,62,role='response'),ebass=P('ebass',BAT_BB,64,role='bass',gain=.75),drums=P('drums',D('backbeat',8),60,role='rhythm',gain=.6)),
 S('C · 盾后的呼吸','33–40 鼓退出一整句，低音改用更长的连接，片段发展不是更快播放A。',piano=P('piano',BAT_C,72),strings=P('strings',H(BAT_H,'held'),45,role='harmony',gain=.43),bass=P('bass',HOME_BASS,58,role='bass',gain=.75)),
 S('推进 · 重组动机','41–48 木管与钢琴回应交接，脉冲和声承接动作密度。',flute=P('flute',transform(BAT_C,replacement={1:'A5:1 G5:.5 F5:.5 D5:1 r:1',5:'Bb5:1 A5:.5 F5:.5 D5:1 r:1'}),76,gain=.68),piano=P('piano',transform(BAT_R,replacement={0:'r:3 A4:.5 C5:.5',1:'r:3 E4:.5 G4:.5',2:'r:3 Bb4:.5 A4:.5',4:'r:3 E5:.5 F5:.5',5:'r:3 D5:.5 F5:.5',6:'r:3 Bb4:.5 A4:.5'}),60,role='response'),nylon=P('nylon',H(BAT_H,'pulse'),59,role='harmony',gain=.8),ebass=P('ebass',BAT_BASS,66,role='bass',gain=.68),drums=P('drums',D('drive',8),60,role='rhythm',gain=.6)),
 S('A″ · 合上阵线','49–56 主主题回归但第二句扩展高点；不是整段音频复制。',piano=P('piano',transform(RESOLVE,replacement={4:'A5:.5 C6:1 D6:.5 C6:.5 A5:.5 G5:.5 r:.5',5:'F5:1 A5:.5 G5:.5 F5:1 D5:.5 r:.5',7:'D5:1 F5:.5 E5:.5 D5:1 A4:.5 r:.5'}),82),strings=P('strings',H(BAT_H,'breath'),51,role='harmony',gain=.43),ebass=P('ebass',BAT_BASS,66,role='bass',gain=.68),drums=P('drums',D('backbeat',8),60,role='rhythm',gain=.6)),
 S('接续 · 仍在前行','57–64 拆解成问答，末拍保留属色彩。鼓的收束仍保持周期节拍。',clarinet=P('clarinet',BAT_C,70),nylon=P('nylon',H(BAT_H,'offbeat'),54,role='harmony',gain=.8),ebass=P('ebass',BAT_BB,60,role='bass',gain=.75),drums=P('drums',D('light',8),50,role='rhythm',gain=.6))])
if __name__=='__main__':
 for compose in (home,basement,battle):
  s=compose();s['revision']=2;(ROOT/f"music/scores/{s['id']}.json").write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print(s['id'],s['length_beats']//4,'bars',sum(len(t['notes']) for t in s['tracks']),'notes')
