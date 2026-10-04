"""Individually authored album. Each entry specifies its own phrases, harmony,
voice handoffs and form. Shared cells are thematic/local accompaniment vocabulary.
Run only to deliberately re-author; normal pipeline reads persisted JSON scores.
"""
from representatives import *
def cat(*lines):return ' | '.join(lines)
def cut(line,a,b):return ' | '.join(bars(line)[a:b])
def harm(inst,chords,style='breath',v=46,g=.55):return P(inst,H(chords,style),v,role='harmony',gain=g)
def low(line,v=48,inst='bass',g=.7):return P(inst,line,v,role='bass',gain=g)
def reply(inst,line,v=48,g=.75):return P(inst,line,v,role='response',gain=g)
def drum(style='light',n=8):return P('drums',D(style,n),50,role='rhythm',gain=.48)
def lead(inst,line,v=64,g=1):return P(inst,line,v,gain=g)
# Independent phrases: long breaths, asymmetric cells, composed endpoints.
TITLE_A='A4:1 D5:2 r:1 | F5:.5 E5:.5 C5:1 A4:1 r:1 | Bb4:1.5 D5:.5 G5:1 r:1 | E5:2 C#5:.5 A4:.5 r:1 | F5:1 A5:1 G5:.5 E5:.5 r:1 | D5:2 F5:.5 E5:.5 C5:1 | Bb4:.5 A4:.5 G4:1 D5:1 r:1 | C#5:1 E5:.5 G5:.5 A4:1 r:1'
TITLE_B='C5:1 F5:.5 A5:.5 C6:1 r:1 | B5:1 G5:.5 E5:.5 D5:1 r:1 | A5:1 F5:1 E5:.5 D5:.5 r:1 | G5:1 Bb5:.5 A5:.5 F5:1 D5:1 | E5:1 C5:.5 G4:.5 C5:1 r:1 | A4:1 C5:.5 F5:.5 A5:1 G5:.5 r:.5 | F5:1 D5:.5 Bb4:.5 E5:1 r:1 | C#5:1 E5:1 A4:1 r:1'
Y_A='r:.5 D5:.5 A4:1 C5:.5 F5:1 r:.5 | E5:.75 D5:.25 C5:1 A4:.5 G4:.5 r:1 | Bb4:1 D5:.5 F5:.5 E5:1 G5:.5 r:.5 | F5:.5 E5:.5 C#5:1 A4:1 r:1 | A5:1 G5:.5 E5:.5 F5:1 r:1 | D5:.5 C5:.5 A4:1 D5:.5 F5:.5 r:1 | G5:1 F5:1 D5:.5 Bb4:.5 r:1 | E5:.5 C#5:.5 A4:1 G4:.5 A4:.5 r:1'
Y_B='G4:1 C5:.5 E5:.5 G5:1 E5:.5 r:.5 | F5:2 A5:.5 G5:.5 r:1 | D5:1 Bb4:.5 D5:.5 F5:1 A5:.5 r:.5 | G5:1 D5:1 Bb4:.5 A4:.5 r:1 | C5:.5 E5:.5 G5:1 B5:1 r:1 | A5:1 F5:.5 E5:.5 D5:1 r:1 | E5:1 G5:.5 F5:.5 D5:1 Bb4:.5 r:.5 | C#5:2 E5:.5 A4:.5 r:1'
Y_LOW='D3:1 F3:1 A2:.5 C3:.5 r:1 | E3:1 C3:.5 B2:.5 G2:1 r:1 | Bb2:1 D3:.5 F3:.5 G3:1 F3:.5 r:.5 | A2:1 C#3:1 E3:.5 G3:.5 r:1 | F3:1 E3:1 C3:.5 A2:.5 r:1 | D3:1 C3:.5 A2:.5 F2:1 r:1 | G2:1 Bb2:.5 D3:.5 F3:1 E3:.5 r:.5 | A2:1 E3:.5 G3:.5 C#3:1 r:1'
COURT_A='D5:.5 r:.5 A4:.5 D5:.5 F5:.75 E5:.25 D5:.5 r:.5 | C5:.5 D5:1 A4:.5 r:.5 C5:.5 E5:.5 r:.5 | F5:.5 A5:.5 G5:1 F5:.5 D5:.5 r:1 | E5:.75 C#5:.25 A4:1 E5:.5 G5:.5 r:1 | F5:.5 r:.5 A5:.5 C6:.5 A5:.75 G5:.25 F5:.5 r:.5 | D5:.5 F5:1 A5:.5 r:.5 F5:.5 D5:.5 r:.5 | G5:1 F5:.5 D5:.5 Bb4:.5 A4:.5 C5:.5 r:.5 | C#5:.5 E5:1 A4:.5 G4:.5 A4:.5 r:1'
COURT_B='E5:1.5 G5:.5 C6:1 r:1 | A5:1 F5:.5 C5:.5 F5:1 r:1 | Bb5:.5 A5:.5 F5:1 D5:1 r:1 | G5:2 F5:.5 D5:.5 r:1 | C5:.5 E5:.5 G5:1 E5:.5 D5:.5 C5:1 | F5:1 A5:1 G5:.5 F5:.5 E5:.5 r:.5 | D5:1 Bb4:.5 A4:.5 G4:1 D5:1 | E5:1 C#5:.5 E5:.5 A5:1 r:1'
COURT_LOW='D2:.5 A2:.5 r:.5 D3:.5 C3:.75 A2:.25 F2:1 | E2:.5 A2:1 C3:.5 E3:.5 r:.5 G2:1 | Bb2:.75 D3:.25 F3:.5 r:.5 D3:.5 C3:.5 Bb2:1 | A2:.5 r:.5 E3:.5 G3:.5 E3:.75 C#3:.25 A2:1 | F2:.5 C3:.5 r:.5 A2:.5 C3:1 E3:.5 F3:.5 | D3:.5 A2:1 C3:.5 F3:.5 r:.5 E3:1 | G2:.75 D3:.25 F3:.5 E3:.5 D3:.5 Bb2:.5 A2:1 | A2:.5 E3:.5 r:.5 C#3:.5 E3:1 G2:.5 A2:.5'
GARDEN_A='D5:2 A4:.5 C5:.5 r:1 | F5:1 E5:.5 D5:.5 C5:1 r:1 | Bb4:.5 D5:.5 G5:2 F5:.5 r:.5 | E5:1 C5:1 A4:1 r:1 | F5:1.5 G5:.5 A5:1 r:1 | G5:.5 F5:.5 D5:1 C5:.5 A4:.5 r:1 | Bb4:1 G4:1 A4:.5 C5:.5 r:1 | D5:2 C#5:.5 E5:.5 r:1'
GARDEN_B='E5:.5 F5:1 r:.5 Bb4:.5 E5:.5 r:1 | D#5:1 B4:.5 F4:.5 r:2 | C5:1 G5:.5 F#5:.5 E5:1 r:1 | B4:1 D5:1 A4:.5 G4:.5 r:1 | Bb4:.5 E5:.5 G5:1 F5:1 r:1 | A4:1 D5:.5 F5:.5 E5:1 C5:1 | G4:1 Bb4:.5 D5:.5 E5:1 r:1 | C#5:.5 E5:.5 A4:1 G4:.5 r:1.5'
GARDEN_LOW='D3:2 A2:.5 C3:.5 r:1 | C3:1 E3:1 G2:.5 r:1.5 | Bb2:1 D3:.5 G3:.5 F3:1 r:1 | A2:2 G2:.5 E2:.5 r:1 | F2:1 C3:1 E3:.5 F3:.5 r:1 | D3:1 A2:.5 G2:.5 F2:1 r:1 | G2:1 Bb2:1 D3:.5 C3:.5 r:1 | A2:1 E3:.5 G3:.5 C#3:1 r:1'
LIB_A='r:1 E5:.5 F5:.5 r:2 | Bb4:1 r:1 E5:.5 r:1.5 | r:.5 F5:.5 B4:1 r:2 | D#5:.5 E5:1.5 r:2 | G5:1 r:1 F5:.5 E5:.5 r:1 | r:2 Bb4:.5 A4:.5 r:1 | F5:.5 E5:.5 r:1 D5:1 r:1 | B4:1 D#5:.5 r:2.5'
LIB_B='G4:1 D5:.5 E5:.5 r:2 | B4:1 G4:1 r:2 | E5:1.5 C5:.5 G4:1 r:1 | F#4:1 A4:.5 B4:.5 r:2 | C5:2 E5:.5 G5:.5 r:1 | F#5:1 D5:.5 B4:.5 G4:1 r:1 | A4:.5 C5:.5 E5:1 D#5:.5 B4:.5 r:1 | F#4:1 A4:.5 D#5:.5 r:2'
LIB_LOW='E2:1 r:2 B2:.5 r:.5 | D#3:1 r:1 A2:.5 B2:.5 r:1 | C3:1 G2:.5 r:2.5 | B2:1 D3:.5 r:2.5 | C3:1 E3:.5 r:1.5 Bb2:.5 r:.5 | D3:1 A2:.5 r:2.5 | F2:1 C3:.5 E3:.5 r:2 | B2:1 A2:.5 F#2:.5 r:2'
CANT_A='F5:.75 E5:.25 D5:.5 A4:.5 C5:1 r:1 | E5:.5 G5:.5 F5:1 E5:.5 C5:.5 r:1 | D5:1 F5:.5 E5:.5 D5:.5 C5:.5 A4:.5 r:.5 | Bb4:.5 D5:.5 G5:1 F5:1 r:1 | E5:.75 D5:.25 C5:1 G4:.5 C5:.5 r:1 | F5:.5 A5:.5 G5:.5 F5:.5 E5:1 r:1 | D5:1 Bb4:.5 G4:.5 A4:1 C5:.5 r:.5 | E5:.5 C#5:.5 A4:1 G4:.5 E4:.5 r:1'
CANT_B='A4:1 C5:2 r:1 | B4:.5 D5:.5 E5:1 G5:1 r:1 | F5:1 D5:.5 A4:.5 C5:1 r:1 | D5:1 Bb4:1 G4:1 r:1 | C5:1 E5:.5 G5:.5 B5:1 r:1 | A5:1 G5:1 E5:.5 D5:.5 r:1 | F5:1 E5:.5 D5:.5 C5:1 Bb4:.5 r:.5 | A4:1 C#5:.5 E5:.5 r:2'
CANT_LOW='F2:.75 A2:.25 C3:1 E3:.5 F3:.5 r:1 | E3:1 C3:.5 B2:.5 G2:1 r:1 | D3:.75 F3:.25 A2:1 C3:.5 D3:.5 r:1 | Bb2:1 D3:.5 F3:.5 G3:1 r:1 | C3:.75 E3:.25 G2:1 B2:.5 C3:.5 r:1 | A2:1 C3:.5 E3:.5 F3:1 r:1 | G2:.75 Bb2:.25 D3:1 E3:.5 D3:.5 r:1 | A2:1 E3:.5 G3:.5 C#3:1 r:1'
RUN_A='A4:.5 D5:.5 r:.5 F5:.5 E5:.5 D5:.5 C5:.5 r:.5 | A4:.75 C5:.25 D5:1 F5:.5 E5:.5 r:1 | F5:.5 A5:1 G5:.5 D5:.5 F5:.5 r:1 | E5:1 C#5:.5 A4:.5 G4:.5 E4:.5 r:1 | A5:.5 C6:.5 A5:1 G5:.5 F5:.5 E5:.5 r:.5 | D5:.75 F5:.25 A5:1 G5:.5 F5:.5 r:1 | D5:.5 G5:1 F5:.5 E5:.5 D5:.5 Bb4:.5 r:.5 | C#5:.5 E5:.5 G5:1 E5:.5 A4:.5 r:1'
RUN_B='C6:2 G5:.5 E5:.5 r:1 | A5:1 G5:.5 F5:.5 E5:1 r:1 | Bb5:1 F5:1 D5:.5 F5:.5 r:1 | G5:1 D5:.5 Bb4:.5 A4:1 r:1 | E5:.5 G5:.5 B5:1 C6:.5 B5:.5 r:1 | A5:1 F5:1 D5:.5 C5:.5 r:1 | G5:.5 F5:.5 E5:1 D5:1 r:1 | C#5:1 E5:1 A5:.5 G5:.5 r:1'
RUN_LOW='D2:.5 A2:.5 C3:.5 D3:.5 r:.5 F3:.5 E3:.5 C3:.5 | A2:.5 E3:.5 G3:.5 E3:.5 r:.5 C3:.5 A2:1 | Bb2:.5 F3:.5 A3:.5 F3:.5 D3:.5 C3:.5 Bb2:1 | A2:.5 E3:.5 r:.5 G3:.5 E3:.5 C#3:.5 A2:1 | F2:.5 C3:.5 E3:.5 F3:.5 A3:.5 G3:.5 F3:1 | D3:.5 A2:.5 C3:.5 F3:.5 r:.5 E3:.5 D3:1 | G2:.5 D3:.5 F3:.5 E3:.5 D3:.5 Bb2:.5 A2:1 | A2:.5 E3:.5 G3:.5 C#3:.5 r:.5 B2:.5 A2:1'
JUN_A='E5:.5 r:.5 F5:.5 E5:.5 Bb4:.5 r:1.5 | B4:.5 E5:.5 D#5:1 r:2 | G5:1 F5:.5 E5:.5 r:1 Bb4:.5 r:.5 | A4:1 F4:.5 E4:.5 r:2 | E5:.5 F5:.5 r:.5 G5:.5 Bb5:1 r:1 | F5:.5 E5:.5 D#5:1 B4:.5 A4:.5 r:1 | Bb4:1 E5:.5 F5:.5 E5:.5 r:1.5 | D#5:1 B4:.5 F#4:.5 r:2'
JUN_B='D5:1 A4:1 C5:.5 F5:.5 r:1 | E5:1 D5:1 C5:.5 A4:.5 r:1 | G4:1 Bb4:.5 D5:.5 F5:1 r:1 | E5:2 A4:1 r:1 | F5:1 A5:.5 G5:.5 F5:.5 E5:.5 r:1 | D5:1 C5:.5 A4:.5 F4:1 r:1 | Bb4:1 A4:.5 G4:.5 E4:1 r:1 | F4:1 E4:.5 D#4:.5 B3:1 r:1'
JUN_LOW='E2:1 B2:.5 E3:.5 r:1 F3:.5 r:.5 | D#3:1 B2:.5 A2:.5 r:2 | C3:1 E3:.5 G2:.5 B2:1 r:1 | B2:1 A2:1 F2:.5 E2:.5 r:1 | C3:1 G2:.5 Bb2:.5 E3:1 r:1 | D3:1 A2:1 C3:.5 r:1.5 | F2:1 C3:.5 E3:.5 A2:1 r:1 | B2:1 F#2:.5 A2:.5 D#3:1 r:1'
SEN_A='A4:1 F5:1 E5:.5 D5:.5 r:1 | C5:1 E5:.5 G5:.5 A5:1 r:1 | G5:1 F5:.5 D5:.5 Bb4:1 r:1 | C5:2 A4:.5 G4:.5 r:1 | F5:.5 G5:.5 A5:1 C6:1 r:1 | A5:1 F5:.5 E5:.5 D5:1 r:1 | G5:1 F5:1 E5:.5 D5:.5 r:1 | C#5:1 A4:1 E5:.5 r:1.5'
SEN_B='A4:.5 D5:1 F5:.5 E5:1 r:1 | C5:1 D5:.5 A4:.5 G4:1 r:1 | F5:1 A5:.5 G5:.5 F5:1 D5:.5 r:.5 | E5:1 C#5:1 A4:1 r:1 | D5:1 F5:.5 A5:.5 G5:1 r:1 | F5:.5 E5:.5 D5:1 C5:1 r:1 | Bb4:1 D5:.5 F5:.5 E5:.5 C#5:.5 r:1 | A4:1 E5:.5 D5:.5 C#5:1 r:1'
SEN_LOW='D3:1 F3:1 E3:.5 D3:.5 r:1 | C3:1 G2:1 B2:.5 C3:.5 r:1 | Bb2:2 D3:.5 F3:.5 r:1 | A2:1 C3:1 E3:.5 G3:.5 r:1 | F2:1 A2:.5 C3:.5 F3:1 r:1 | D3:1 C3:.5 A2:.5 F2:1 r:1 | G2:1 Bb2:.5 D3:.5 F3:1 E3:.5 r:.5 | A2:1 G2:.5 E2:.5 C#3:1 r:1'
LAB_A='E5:.5 B4:.5 F5:.5 r:.5 E5:1 Bb4:.5 r:.5 | F5:.5 E5:.5 D#5:.5 B4:.5 r:1 A4:.5 r:.5 | G5:.75 F#5:.25 E5:.5 G5:.5 B5:1 r:1 | A5:.5 F5:.5 E5:1 B4:.5 D5:.5 r:1 | Bb4:.5 E5:.5 G5:.5 F5:.5 r:.5 E5:.5 B4:.5 r:.5 | D5:1 A4:.5 F4:.5 A4:1 C5:.5 r:.5 | E5:.5 F5:.5 A5:.5 G5:.5 E5:1 r:1 | D#5:.5 F#5:.5 B5:1 A5:.5 F#5:.5 r:1'
LAB_B='B4:.5 E5:1.5 G5:.5 F#5:.5 E5:.5 r:.5 | D5:1 E5:.5 B4:.5 A4:1 r:1 | G5:.5 B5:1 A5:.5 G5:.5 E5:.5 r:1 | F#5:1 B4:1 D#5:.5 F#5:.5 r:1 | E5:.5 G5:.5 B5:1 D6:.5 B5:.5 A5:1 | G5:1 F#5:.5 E5:.5 D5:1 r:1 | C5:.5 E5:1 G5:.5 F#5:.5 D#5:.5 B4:.5 r:.5 | E5:1 F#5:.5 B4:.5 D#5:1 r:1'
LAB_LOW='E2:.75 B2:.25 E3:.5 r:.5 F3:.5 E3:.5 B2:1 | D#3:.5 B2:.5 A2:.5 F#2:.5 B2:1 r:1 | C3:.75 G2:.25 B2:.5 E3:.5 G3:.5 F#3:.5 E3:1 | B2:.5 D3:.5 G3:.5 F3:.5 E3:1 r:1 | C3:.75 G2:.25 Bb2:.5 E3:.5 G3:.5 E3:.5 C3:1 | D3:.5 A2:.5 C3:.5 D3:.5 F3:1 r:1 | F2:.75 C3:.25 E3:.5 A2:.5 C3:.5 E3:.5 F3:1 | B2:.5 F#2:.5 A2:.5 B2:.5 D#3:1 r:1'
ADMIN_A='E4:1 r:1 F4:.5 Bb4:.5 r:1 | B4:1 D#5:.5 E5:.5 r:2 | G4:1 C5:.5 F#5:.5 E5:1 r:1 | D5:1 B4:1 A4:.5 r:1.5 | Bb4:.5 E5:1 F5:.5 G5:1 r:1 | F5:1 D5:.5 A4:.5 C5:1 r:1 | E5:.5 F5:.5 A4:1 Bb4:.5 E5:.5 r:1 | D#5:1 B4:.5 F#4:.5 r:2'
ADMIN_B='A4:1 D5:1 F5:.5 E5:.5 r:1 | C5:1 D5:.5 A4:.5 E5:1 r:1 | F5:1 A5:1 G5:.5 F5:.5 r:1 | E5:1 C#5:1 A4:.5 G4:.5 r:1 | D5:.5 F5:.5 A5:1 C6:1 r:1 | Bb5:1 A5:.5 F5:.5 D5:1 r:1 | G5:1 F5:.5 E5:.5 D5:1 r:1 | F5:.5 E5:.5 D#5:1 B4:1 r:1'
ADMIN_LOW='E2:2 B2:.5 E3:.5 r:1 | D#3:1 A2:1 F#2:.5 B2:.5 r:1 | C3:2 G2:.5 B2:.5 r:1 | B2:1 D3:1 A2:.5 G2:.5 r:1 | C3:1 Bb2:.5 G2:.5 E2:1 r:1 | D3:1 C3:.5 A2:.5 F2:1 r:1 | F2:1 A2:1 C3:.5 E3:.5 r:1 | B2:1 D#3:.5 F#3:.5 A2:1 r:1'
BOSS_A='D5:.5 A4:.5 r:.5 F5:.5 E5:.5 D5:.5 C#5:.5 r:.5 | E5:.5 Bb4:.5 F5:1 E5:.5 D#5:.5 r:1 | F5:.5 A5:.5 D6:.75 C6:.25 A5:.5 G5:.5 F5:.5 r:.5 | E5:.5 C#5:.5 A4:1 G5:.5 E5:.5 r:1 | D5:.5 F5:.5 A5:.5 Bb5:.5 A5:.75 G5:.25 F5:.5 r:.5 | E5:.5 F5:.5 Bb4:1 G5:.5 F5:.5 E5:.5 r:.5 | D5:.5 G5:.5 F5:1 E5:.5 C#5:.5 A4:.5 r:.5 | E5:.5 C#5:.5 Bb4:.5 A4:.5 G4:1 r:1'
BOSS_B='A5:1 G5:.5 F5:.5 D5:1 r:1 | G5:1 E5:.5 C5:.5 G4:1 r:1 | Bb5:1 A5:.5 G5:.5 F5:1 D5:.5 r:.5 | A5:1 E5:1 C#5:.5 G4:.5 r:1 | F5:.5 A5:.5 C6:1 D6:1 r:1 | Bb5:1 F5:.5 D5:.5 E5:1 r:1 | G5:1 F5:.5 E5:.5 D5:.5 Bb4:.5 r:1 | A4:.5 C#5:.5 E5:1 G5:.5 E5:.5 r:1'
BOSS_LOW='D2:.5 A2:.5 D3:.75 C#3:.25 D3:.5 F3:.5 E3:.5 r:.5 | E2:.5 B2:.5 Bb2:.5 E3:.5 F3:.5 E3:.5 D#3:1 | Bb2:.5 D3:.5 F3:.75 A3:.25 G3:.5 F3:.5 D3:1 | A2:.5 E3:.5 G3:.5 E3:.5 C#3:.5 A2:.5 G2:1 | F2:.5 C3:.5 A2:.5 F3:.5 E3:.5 C3:.5 A2:1 | Bb2:.5 F3:.5 E3:.5 D3:.5 C3:.5 Bb2:.5 A2:1 | G2:.5 D3:.5 F3:.5 E3:.5 D3:.5 Bb2:.5 A2:1 | A2:.5 E3:.5 C#3:.5 G3:.5 E3:.5 Bb2:.5 A2:1'
FIN_A='A4:.5 D5:1 F5:.5 E5:.5 D5:.5 A4:.5 r:.5 | C5:.75 E5:.25 G5:1 F5:.5 E5:.5 D5:.5 r:.5 | F5:.5 A5:1 C6:.5 Bb5:.5 A5:.5 G5:.5 r:.5 | E5:1 C#5:.5 A4:.5 G4:1 r:1 | D5:.5 F5:.5 A5:.5 C6:.5 D6:1 A5:.5 r:.5 | Bb5:1 A5:.5 F5:.5 D5:1 r:1 | G5:.5 F5:.5 E5:1 D5:.5 C#5:.5 A4:.5 r:.5 | D5:1 E5:.5 G5:.5 C#5:1 r:1'
FIN_B='F5:1 A5:.5 G5:.5 E5:1 r:1 | G5:1 E5:.5 C5:.5 D5:1 r:1 | Bb5:1 A5:.5 F5:.5 D5:1 r:1 | A5:1 G5:.5 E5:.5 C#5:1 r:1 | C6:1 A5:.5 G5:.5 F5:1 r:1 | Bb5:1 D6:.5 C6:.5 A5:1 F5:1 | G5:1 E5:.5 D5:.5 Bb4:1 r:1 | E5:.5 C#5:.5 A4:1 G4:.5 E4:.5 r:1'
SUS_A='r:2 E5:.5 F5:.5 r:1 | Bb4:.5 r:1.5 B4:.5 r:1.5 | E5:1 r:1 F5:.5 r:1.5 | r:1 D#5:.5 E5:.5 r:2 | G5:.5 F5:.5 r:2 E5:.5 r:.5 | r:1 Bb4:1 A4:.5 r:1.5 | F5:.5 E5:.5 r:1 Bb4:1 r:1 | B4:.5 D#5:.5 r:3'
SUS_B='C5:1 r:1 G5:.5 F#5:.5 r:1 | B4:1 D5:.5 r:2.5 | A4:1 C5:.5 E5:.5 r:2 | Bb4:.5 E5:.5 G5:1 r:2 | F5:1 A4:1 r:2 | C5:1 F5:.5 E5:.5 r:2 | Bb4:1 A4:.5 F4:.5 r:2 | F#4:.5 A4:.5 D#5:1 r:2'
END_A='D5:1 A4:.5 C5:.5 F5:1 r:1 | E5:1 C5:.5 A4:.5 G4:1 r:1 | Bb4:1 D5:.5 G5:.5 F5:1 r:1 | C5:2 A4:1 r:1 | F5:1 A5:.5 G5:.5 F5:1 E5:.5 r:.5 | D5:1 F5:.5 E5:.5 C5:1 r:1 | Bb4:1 A4:.5 G4:.5 A4:1 C5:.5 r:.5 | D5:2 C#5:.5 E5:.5 r:1'
END_B='A4:1 D5:1 F#5:.5 E5:.5 r:1 | C#5:1 D5:.5 A4:.5 B4:1 r:1 | F#5:1 A5:.5 G5:.5 F#5:1 E5:.5 r:.5 | E5:1 C#5:1 A4:1 r:1 | D5:.5 F#5:.5 A5:1 B5:1 r:1 | G5:1 F#5:.5 E5:.5 D5:1 r:1 | B4:1 D5:.5 G5:.5 E5:1 r:1 | C#5:1 E5:.5 A4:.5 D5:1 r:1'
END_H=['F#3 A3 D4 E4','E3 A3 C#4 E4','D3 G3 B3 D4','E3 A3 C#4 E4','F#3 A3 D4 F#4','D3 G3 B3 D4','E3 G3 B3 D4','E3 G3 A3 C#4']
END_LOW='D3:1 A2:1 C#3:.5 D3:.5 r:1 | C#3:1 E3:.5 A2:.5 G2:1 r:1 | B2:1 D3:.5 G3:.5 F#3:1 r:1 | A2:1 E3:1 G3:.5 E3:.5 r:1 | F#2:1 A2:.5 C#3:.5 D3:1 r:1 | G2:1 B2:.5 D3:.5 G3:1 F#3:.5 r:.5 | E3:1 D3:.5 B2:.5 G2:1 r:1 | A2:1 E3:.5 G3:.5 C#3:1 r:1'
SUM_A='A4:.5 C5:.5 F5:1 E5:.5 D5:.5 r:1 | C5:.75 E5:.25 G5:1 A5:.5 G5:.5 r:1 | F5:.5 D5:.5 A4:1 C5:.5 D5:.5 r:1 | Bb4:.5 D5:.5 F5:1 G5:.5 F5:.5 r:1 | E5:1 C5:.5 G4:.5 C5:1 r:1 | F5:.5 A5:.5 C6:1 A5:.5 G5:.5 r:1 | F5:1 D5:.5 Bb4:.5 E5:1 r:1 | C#5:.5 E5:.5 A5:1 G5:.5 E5:.5 r:1'
SUM_B='D5:.5 F5:.5 A5:1 C6:.5 A5:.5 G5:1 | E5:1 G5:.5 B5:.5 C6:1 r:1 | Bb5:1 F5:.5 D5:.5 F5:1 r:1 | A5:1 E5:.5 C#5:.5 A4:1 r:1 | F5:.5 A5:.5 C6:1 D6:.5 C6:.5 A5:1 | Bb5:1 A5:.5 F5:.5 D5:1 r:1 | G5:1 F5:.5 E5:.5 D5:1 r:1 | C#5:1 E5:.5 G5:.5 A4:1 r:1'
Y_H=['F3 A3 D4 F4','E3 G3 C4 E4','D3 F3 Bb3 D4','E3 G3 A3 C#4','A3 C4 F4 G4','F3 A3 D4 E4','F3 Bb3 D4 G4','G3 A3 C#4 E4']
G_H=['A3 D4 E4 F4','G3 C4 D4 E4','G3 Bb3 D4 F4','G3 A3 C4 E4','A3 C4 F4 A4','A3 C4 D4 F4','G3 Bb3 D4 E4','G3 A3 C#4 E4']
J_H=['G3 B3 E4 F4','F#3 A3 B3 D#4','G3 C4 E4 G4','F3 A3 B3 E4','G3 Bb3 C4 E4','F3 A3 D4 E4','F3 A3 C4 E4','F#3 A3 B3 D#4']
L_H=['B3 E4 F4 G4','A3 B3 D#4 F#4','G3 C4 E4 F#4','G3 B3 D4 E4','Bb3 C4 E4 G4','A3 D4 E4 F4','A3 C4 E4 F4','A3 B3 D#4 F#4']
A_H=['G3 B3 E4 G4','F#3 A3 B3 D#4','G3 C4 E4 F#4','G3 B3 D4 F4','G3 Bb3 C4 E4','F3 A3 C4 D4','F3 A3 C4 E4','F#3 A3 B3 D#4']

def title():
 return score(CUES['title'],[
 S('信封 · 尚未出现的人','1–8 校园动机扩展为留白的钟楼旋律，竖琴不持续铺底。',piano=lead('piano',TITLE_A,65),harp=harm('harp',HOME_H1,'breath',43,.62),bass=low(GARDEN_LOW,45)),
 S('名字 · 主题全貌','9–16 校园主题交给木管；钢琴只补空隙，形成识别点。',clarinet=lead('clarinet',CAMPUS,57,.78),piano=reply('piano',HOME_REPLY,53),bass=low(SEN_LOW,46)),
 S('钟影 · 来信的背面','17–24 侵蚀主题完整闯入E区域，撤去木管与温暖低音。',electric=lead('electric',INTRUSION,53,.8),cello=harm('cello',EXP_H,'held',40,.35),bass=low(EXP_LOW,42)),
 S('开门 · 明亮远景','25–32 新的F区长句由钢琴展开，弦乐只托中段而不加鼓。',piano=lead('piano',TITLE_B,70),strings=harm('strings',HOME_H2,'breath',44,.38),bass=low(HOME_BB,49)),
 S('留信 · 回到门前','33–40 首段改写高点、缩短结束，A属和声导回D。',piano=lead('piano',transform(TITLE_A,replacement={2:'G5:1 F5:.5 D5:.5 Bb4:1 r:1',4:'A5:1 C6:.5 A5:.5 G5:1 r:1',7:'E5:1 C#5:.5 A4:.5 G4:1 r:1'}),63),harp=harm('harp',HOME_H1,'dialogue',42,.62),bass=low(GARDEN_LOW,43))])
def yifu():
 return score(CUES['yifu'],[
 S('A · 玻璃折光','1–8 弱起木管与拨弦错开，旋律改写校园短短长。',flute=lead('flute',Y_A,58,.66),nylon=harm('nylon',Y_H,'dialogue'),bass=low(Y_LOW)),
 S('B · 风穿过连廊','9–16 高音钢琴展开连续远景，低音由C/F区域出发。',piano=lead('piano',Y_B,70),harp=harm('harp',HOME_H2,'breath',44,.62),bass=low(HOME_BB)),
 S('回声 · 空中花园','17–24 单簧管下行回答，钢琴断句落在第四拍。',clarinet=lead('clarinet',transform(Y_B,octave=-1,replacement={0:'E5:1 G5:.5 C6:.5 B5:1 r:1',4:'C6:1 B5:.5 G5:.5 E5:1 r:1',7:'A4:1 C#5:.5 E5:.5 r:2'}),60,.75),piano=reply('piano',HOME_REPLY),bass=low(transform(Y_LOW,replacement={0:'E3:1 G3:.5 E3:.5 C3:1 r:1',4:'C3:1 A2:1 F2:1 r:1'}),44)),
 S('A′ · 反射的同伴','25–32 校园完整主题由钢琴接回，取代弱起碎片。',piano=lead('piano',transform(CAMPUS,replacement={3:'C5:1 E5:.5 G5:.5 A5:1 r:1',7:'D5:1 F5:.5 E5:.5 C#5:1 r:1'}),68),nylon=harm('nylon',Y_H,'offbeat'),bass=low(Y_LOW)),
 S('余风 · 回到走廊','33–40 长笛低密度缩句，末句减音留下一次弱起位置。',flute=lead('flute',transform(Y_A,replacement={0:'r:1 D5:1 A4:1 r:1',2:'Bb4:1 D5:1 r:2',4:'A5:1 G5:.5 E5:.5 r:2',6:'G5:1 D5:1 r:2',7:'C#5:1 A4:.5 G4:.5 r:2'}),55,.66),harp=harm('harp',Y_H,'breath',42,.62),bass=low(Y_LOW,43))])
def basketball():
 return score(CUES['basketball'],[
 S('运球 · A','1–8 切分不落满强拍，马林巴与贝斯共同定重心。',marimba=lead('marimba',COURT_A,74),nylon=harm('nylon',BAT_H,'offbeat',54,.75),ebass=low(COURT_LOW,61,'ebass'),drums=drum('backbeat')),
 S('传球 · A′','9–16 单簧管接棒并改变短句终点，打击乐改轻。',clarinet=lead('clarinet',transform(COURT_A,replacement={1:'D5:1 F5:.5 E5:.5 C5:.5 A4:.5 r:1',5:'A5:.5 F5:1 D5:.5 C5:1 r:1'}),66,.75),marimba=reply('marimba',BAT_R,51),ebass=low(COURT_LOW,57,'ebass'),drums=drum()),
 S('暂停 · B','17–24 钢琴长线对照运球切分，鼓退出，保留会呼吸的低音。',piano=lead('piano',COURT_B,72),nylon=harm('nylon',BAT_HB,'breath',50,.75),bass=low(HOME_BB,50)),
 S('约定 · 希望主题','25–32 以完整主题解释赛场的抵抗动机，律动逐渐回来。',clarinet=lead('clarinet',RESOLVE,66,.75),nylon=harm('nylon',BAT_H,'dialogue',54,.75),ebass=low(BAT_BB,58,'ebass'),drums=drum('brush')),
 S('快攻 · A″','33–40 马林巴回归变更高点，低音逆向变化而不复制第一段。',marimba=lead('marimba',transform(COURT_A,replacement={2:'A5:.5 C6:.5 A5:1 F5:.5 D5:.5 r:1',4:'C6:1 A5:.5 G5:.5 F5:.75 E5:.25 D5:.5 r:.5',7:'E5:.5 G5:.5 A5:1 E5:.5 C#5:.5 r:1'}),76),nylon=harm('nylon',BAT_H,'pulse',53,.75),ebass=low(transform(COURT_LOW,replacement={0:'F2:.5 A2:.5 C3:1 D3:.5 C3:.5 A2:1',4:'A2:.5 C3:.5 F3:1 E3:.5 C3:.5 A2:1'}),62,'ebass'),drums=drum('drive')),
 S('回线 · 重新发球','41–48 木管把长句收拢，终拍休止给第一拍运球。',clarinet=lead('clarinet',transform(COURT_B,octave=-1,replacement={3:'G5:1 F5:.5 D5:.5 r:2',7:'C#5:1 E5:.5 G5:.5 A4:.5 r:1.5'}),61,.75),nylon=harm('nylon',BAT_HB,'offbeat',49,.75),ebass=low(BAT_BB,55,'ebass'),drums=drum())])
def garden():
 return score(CUES['garden'],[
 S('枝叶 · A','1–8 扩大校园主题时值，竖琴与木管交换呼吸。',flute=lead('flute',GARDEN_A,54,.66),harp=harm('harp',G_H,'dialogue',44,.62),bass=low(GARDEN_LOW,44)),
 S('根系 · 隐流','9–16 电钢新半音线索，和声逐步转入古树下的不确定性。',electric=lead('electric',GARDEN_B,52,.85),cello=harm('cello',EXP_H,'breath',42,.4),bass=low(EXP_LOW,43)),
 S('古树 · 内部纹理','17–24 单簧管接低音区侵蚀动机，竖琴回应代替完整和弦。',clarinet=lead('clarinet',transform(INTRUSION,octave=-1,replacement={3:'E5:1 G5:.5 F5:.5 r:2',7:'F5:.5 E5:.5 D5:1 A4:.5 r:1.5'}),56,.73),harp=reply('harp',EXP_REPLY,48,.62),bass=low(JUN_LOW,42)),
 S('新叶 · A′','25–32 钢琴重述温暖线条，将第七句打开而非直接结束。',piano=lead('piano',transform(GARDEN_A,replacement={2:'D5:1 G5:1 A5:.5 G5:.5 r:1',5:'A5:1 F5:.5 E5:.5 D5:1 r:1',6:'G5:1 F5:1 E5:.5 D5:.5 r:1'}),66),strings=harm('strings',G_H,'breath',42,.38),bass=low(SEN_LOW,47)),
 S('树影 · 未消失的记忆','33–40 A与半音线索结合，最后两小节明确导回D。',flute=lead('flute',transform(GARDEN_A,replacement={1:'E5:1 F5:.5 E5:.5 C5:1 r:1',4:'A5:1 G5:.5 F5:.5 E5:1 r:1',7:'C#5:1 E5:.5 A4:.5 r:2'}),53,.66),harp=harm('harp',G_H,'breath',42,.62),bass=low(GARDEN_LOW,43))])
def library():
 return score(CUES['library'],[
 S('索引 · 稀疏问题','1–8 钟琴短动机与非连续低音，空白属于书架。',celesta=lead('celesta',LIB_A,53,.9),cello=harm('cello',L_H,'breath',36,.32),bass=low(LIB_LOW,39)),
 S('夹页 · 人的字迹','9–16 单簧管独立G区长句，电钢只在空隙回应。',clarinet=lead('clarinet',LIB_B,49,.67),electric=reply('electric',EXP_REPLY,42,.6),bass=low(EXP_LOWB,40)),
 S('机关 · 分解与移动','17–24 钟琴把动机移至弱拍、扩展尾部；和声更换转位。',celesta=lead('celesta',transform(LIB_A,replacement={0:'r:2 E5:.5 F5:.5 Bb4:.5 r:.5',2:'B4:.5 E5:.5 G5:1 F5:.5 r:1.5',4:'F5:1 E5:.5 D#5:.5 B4:1 r:1',6:'A4:.5 Bb4:.5 E5:1 F5:.5 E5:.5 r:1'}),56,.9),electric=harm('electric',A_H,'dialogue',40,.5),bass=low(transform(LIB_LOW,replacement={0:'E3:1 B2:.5 G2:.5 r:2',4:'Bb2:1 C3:.5 E3:.5 r:2'}),41)),
 S('合书 · 问题仍在','25–32 木管缩短长句，最后B属引向下一次E疑问。',clarinet=lead('clarinet',transform(LIB_B,replacement={0:'G4:1 B4:.5 D5:.5 r:2',2:'E5:1 C5:.5 G4:.5 r:2',4:'C5:1 E5:.5 G5:.5 r:2',7:'D#5:1 B4:.5 F#4:.5 r:2'}),48,.67),cello=harm('cello',L_H,'held',35,.32),bass=low(LIB_LOW,38))])
def canteen():
 return score(CUES['canteen'],[
 S('热汤 · A','1–8 拨弦旋律带轻快附点，钢琴用中音区对话和弦。',nylon=lead('nylon',CANT_A,74),piano=harm('piano',HOME_H2,'dialogue',52,.9),bass=low(CANT_LOW,49),drums=drum('brush')),
 S('排队 · 延伸','9–16 马林巴回答，旋律改写落点与高音；拨弦退出。',marimba=lead('marimba',transform(CANT_A,replacement={0:'A5:.5 G5:.5 F5:1 E5:.5 D5:.5 r:1',3:'Bb4:1 D5:.5 G5:.5 F5:.5 E5:.5 r:1',7:'C#5:1 E5:.5 G5:.5 A4:1 r:1'}),63,.8),piano=harm('piano',HOME_H2,'offbeat',48,.9),bass=low(CANT_LOW,46)),
 S('未寄出的答案 · B','17–24 单簧管拉长线条，撤鼓，在日常中停顿。',clarinet=lead('clarinet',CANT_B,56,.74),piano=harm('piano',HOME_H2,'breath',48,.9),bass=low(HOME_BB,44)),
 S('伙伴 · 校园回声','25–32 钢琴陈述校园主题，F区域重新落回D，鼓恢复轻触。',piano=lead('piano',transform(CAMPUS,replacement={4:'A5:1 G5:.5 F5:.5 E5:1 r:1',7:'D5:1 F5:.5 E5:.5 C#5:1 r:1'}),68,.9),nylon=harm('nylon',HOME_H1,'breath',47,1),bass=low(Y_LOW,46),drums=drum('brush')),
 S('收桌 · A′','33–40 拨弦回归，高点收敛；尾句去掉两音导回F/D共同音。',nylon=lead('nylon',transform(CANT_A,replacement={1:'G5:1 E5:.5 C5:.5 r:2',4:'E5:1 C5:1 A4:.5 r:1.5',5:'F5:.5 A5:.5 G5:1 F5:1 r:1',7:'C#5:1 A4:1 r:2'}),68),piano=harm('piano',HOME_H2,'dialogue',45,.9),bass=low(CANT_LOW,44))])
def playground():
 return score(CUES['playground'],[
 S('起跑 · A','1–8 木管短句带空拍；低音运动构成跑动而非加快战斗曲。',flute=lead('flute',RUN_A,65,.65),nylon=harm('nylon',BAT_H,'offbeat',55,.7),ebass=low(RUN_LOW,59,'ebass'),drums=drum('drive')),
 S('迎风 · B','9–16 钢琴高音长句展开视野，拍点不再密集。',piano=lead('piano',RUN_B,76),strings=harm('strings',BAT_HB,'breath',44,.38),ebass=low(BAT_BB,55,'ebass'),drums=drum()),
 S('岔路 · 动机切片','17–24 从A第二句发展，单簧管下行与钢琴空隙回应。',clarinet=lead('clarinet',transform(RUN_A,octave=-1,replacement={0:'D5:1 F5:.5 E5:.5 C5:.5 A4:.5 r:1',2:'A5:1 G5:.5 F5:.5 D5:1 r:1',4:'C6:1 A5:.5 G5:.5 F5:.5 E5:.5 r:1'}),67,.74),piano=reply('piano',BAT_R,49),ebass=low(RUN_LOW,54,'ebass'),drums=drum('backbeat')),
 S('看台 · 伙伴','25–32 校园主题缓下呼吸但速度不变，鼓完全退出。',piano=lead('piano',transform(CAMPUS,replacement={3:'C5:1 A4:1 G4:1 r:1',7:'D5:1 A4:.5 C#5:.5 E5:1 r:1'}),68),nylon=harm('nylon',HOME_H1,'dialogue',49,.7),bass=low(SEN_LOW,51)),
 S('冲刺 · A′','33–40 A高点上移，木管与贝斯反向，鼓维持同一网格。',flute=lead('flute',transform(RUN_A,replacement={2:'A5:.5 C6:1 B5:.5 A5:.5 F5:.5 r:1',4:'C6:1 A5:.5 G5:.5 F5:.5 E5:.5 D5:.5 r:.5',7:'A5:1 G5:.5 E5:.5 C#5:1 r:1'}),68,.65),nylon=harm('nylon',BAT_H,'pulse',55,.7),ebass=low(transform(RUN_LOW,replacement={2:'D3:.5 F3:.5 Bb2:1 A2:.5 G2:.5 F2:1',4:'A2:.5 C3:.5 F3:1 E3:.5 C3:.5 A2:1'}),60,'ebass'),drums=drum('drive')),
 S('长跑 · 接续','41–48 B缩句交给单簧管，下行导回下一轮。',clarinet=lead('clarinet',transform(RUN_B,octave=-1,replacement={0:'C6:1 G5:1 E5:.5 r:1.5',4:'G5:1 E5:1 C5:.5 r:1.5',7:'E5:1 C#5:.5 A4:.5 r:2'}),63,.74),nylon=harm('nylon',BAT_HB,'offbeat',48,.7),ebass=low(BAT_BB,53,'ebass'),drums=drum())])
def junior():
 return score(CUES['junior'],[
 S('广播 · A','1–8 电钢碎拍与半音，低音保留向下的重心。',electric=lead('electric',JUN_A,58,.8),pad=harm('pad',J_H,'breath',36,.28),bass=low(JUN_LOW,46)),
 S('走廊 · A的失真','9–16 单簧管低区重排停顿，电钢只给三个短回答。',clarinet=lead('clarinet',transform(JUN_A,octave=-1,replacement={0:'r:1 E5:.5 F5:.5 Bb4:1 r:1',3:'r:1 A4:1 F4:.5 E4:.5 r:1',5:'F5:1 E5:.5 D#5:.5 r:2'}),58,.76),electric=reply('electric',transform(EXP_REPLY,replacement={1:'r:4',3:'r:4',5:'r:4',7:'r:4'}),45,.8),bass=low(EXP_LOW,43)),
 S('名字 · B','17–24 校园主题变成犹疑的慢句，钢琴与真实木质拨弦替代pad。',piano=lead('piano',JUN_B,64),nylon=harm('nylon',HOME_H1,'dialogue',42,.58),bass=low(SEN_LOW,43)),
 S('内讧 · 撕开的语句','25–32 原主题间隙加入向上延伸，疑问加深但不增加响度。',electric=lead('electric',transform(JUN_A,replacement={2:'G5:.5 Bb5:1 A5:.5 F5:.5 E5:.5 r:1',4:'Bb4:.5 E5:.5 F5:1 G5:.5 F5:.5 r:1',6:'F5:1 E5:.5 Bb4:.5 A4:1 r:1'}),57,.8),cello=harm('cello',J_H,'held',39,.38),bass=low(JUN_LOW,45)),
 S('未说完 · 回环','33–40 B的前半与A的残片相接，D#属音回到E。',clarinet=lead('clarinet',cat(cut(JUN_B,0,4),cut(transform(JUN_A,replacement={7:'D#5:1 B4:1 F#4:.5 r:1.5'}),4,8)),54,.76),electric=harm('electric',J_H,'breath',40,.8),bass=low(EXP_LOW,41))])
def senior():
 return score(CUES['senior'],[
 S('楼梯 · A','1–8 钢琴长句追忆，不用鼓制造情绪。',piano=lead('piano',SEN_A,66),cello=harm('cello',HOME_H1,'breath',40,.36),bass=low(SEN_LOW,45)),
 S('窗厅 · B','9–16 单簧管将希望动机拉成长呼吸，尼龙弦连接。',clarinet=lead('clarinet',SEN_B,57,.75),nylon=harm('nylon',BAT_H,'dialogue',44,.6),bass=low(GARDEN_LOW,44)),
 S('物理办公室 · 对话','17–24 校园主题换给高区钢琴，回应只发生在主句结束。',piano=lead('piano',transform(CAMPUS,replacement={0:'D5:1 A4:.5 C5:.5 F5:1 r:1',3:'C5:1 E5:.5 G5:.5 A4:1 r:1',7:'D5:1 F5:.5 E5:.5 C#5:1 r:1'}),68),clarinet=reply('clarinet',HOME_REPLY,43,.75),bass=low(Y_LOW,46)),
 S('旧日光 · A′','25–32 主句高点留住，低音向反方向转位，弦乐接续。',piano=lead('piano',transform(SEN_A,replacement={1:'G5:1 A5:.5 G5:.5 E5:1 r:1',4:'C6:1 A5:1 G5:.5 F5:.5 r:1',6:'F5:1 E5:.5 D5:.5 Bb4:1 r:1'}),69),strings=harm('strings',HOME_H1,'held',39,.34),bass=low(transform(SEN_LOW,replacement={0:'F3:1 E3:.5 D3:.5 A2:1 r:1',4:'A2:1 C3:.5 F3:.5 E3:1 r:1'}),46)),
 S('七层 · 接近答案','33–40 B尾句不再上冲，木管接回属和声。',clarinet=lead('clarinet',transform(SEN_B,replacement={2:'F5:1 A5:.5 G5:.5 r:2',4:'D5:1 F5:1 E5:.5 r:1.5',7:'C#5:1 E5:.5 A4:.5 r:2'}),54,.75),nylon=harm('nylon',BAT_H,'breath',42,.6),bass=low(GARDEN_LOW,42))])
def laboratory():
 return score(CUES['laboratory'],[
 S('误差 · A','1–8 电钢错位短句，轻踩镲只提示系统脉冲。',electric=lead('electric',LAB_A,62,.85),pizz=harm('pizz',L_H,'pulse',46,.55),ebass=low(LAB_LOW,53,'ebass'),drums=drum('ticks')),
 S('轨道 · 延伸','9–16 马林巴把片段扩成上行星图，电钢撤去。',marimba=lead('marimba',transform(LAB_A,replacement={2:'B5:1 G5:.5 E5:.5 F#5:1 r:1',4:'G5:.5 B5:.5 D6:1 C6:.5 B5:.5 r:1',7:'F#5:1 D#5:.5 B4:.5 A4:1 r:1'}),67),pizz=harm('pizz',L_H,'offbeat',45,.55),ebass=low(LAB_LOW,52,'ebass'),drums=drum()),
 S('驾驶 · B','17–24 希望主题重新写为E区回应，钢琴不模仿电子震荡。',piano=lead('piano',LAB_B,74),strings=harm('strings',EXP_HB,'breath',43,.35),ebass=low(EXP_LOWB,55,'ebass'),drums=drum('backbeat')),
 S('天文台 · 悬空','25–32 撤鼓、木管长音与电钢回答，保持宇宙尺度的空白。',clarinet=lead('clarinet',transform(LAB_B,octave=-1,replacement={0:'E5:2 G5:.5 B5:.5 r:1',2:'B5:1 G5:1 E5:.5 r:1.5',4:'G5:1 B5:1 D6:.5 r:1.5',7:'D#5:1 F#5:.5 B4:.5 r:2'}),57,.73),electric=reply('electric',EXP_REPLY,47,.85),bass=low(ADMIN_LOW,46)),
 S('校准 · A′','33–40 电钢回归但半音问题被长线回应，贝斯用倒置轮廓。',electric=lead('electric',transform(LAB_A,replacement={0:'E5:.5 G5:.5 B5:1 F5:.5 E5:.5 r:1',3:'D5:1 B4:.5 G4:.5 E5:1 r:1',6:'A5:1 G5:.5 E5:.5 F5:.5 E5:.5 r:1'}),62,.85),pizz=harm('pizz',L_H,'dialogue',46,.55),ebass=low(transform(LAB_LOW,replacement={0:'G2:.5 B2:.5 E3:1 D#3:.5 B2:.5 G2:1',4:'E3:.5 C3:.5 Bb2:1 G2:.5 C3:.5 E3:1'}),53,'ebass'),drums=drum('ticks')),
 S('再扫描 · 接续','41–48 B前句与A末句组合为明确接缝，镲退出末拍。',piano=lead('piano',cat(cut(LAB_B,0,4),cut(transform(LAB_A,replacement={7:'D#5:1 B4:.5 F#4:.5 r:2'}),4,8)),69),pizz=harm('pizz',L_H,'breath',42,.55),ebass=low(EXP_LOW,48,'ebass'),drums=drum())])
def admin():
 return score(CUES['admin'],[
 S('门 · A','1–8 低区单簧管与大提琴呈现证据，不急于给出战斗力度。',clarinet=lead('clarinet',ADMIN_A,55,.75),cello=harm('cello',A_H,'held',38,.37),bass=low(ADMIN_LOW,43)),
 S('密钥 · 线索靠近','9–16 电钢改写侵蚀主题的落点，原先碎片形成较长句。',electric=lead('electric',transform(INTRUSION,replacement={1:'F5:1 E5:.5 B4:.5 A4:1 r:1',3:'D#5:1 E5:1 G5:.5 r:1.5',7:'F5:1 E5:.5 D#5:.5 B4:1 r:1'}),53,.8),cello=harm('cello',L_H,'breath',37,.37),bass=low(JUN_LOW,43)),
 S('选择 · B','17–24 希望主题在D区域第一次正面回答，钢琴宽音区但不齐奏。',piano=lead('piano',ADMIN_B,69),strings=harm('strings',BAT_H,'breath',42,.35),bass=low(SEN_LOW,47)),
 S('证词 · A′','25–32 单簧管问句增添向上的高点，低音反向重排。',clarinet=lead('clarinet',transform(ADMIN_A,replacement={0:'E4:1 G4:.5 B4:.5 F5:1 r:1',4:'G5:1 F5:.5 E5:.5 Bb4:1 r:1',6:'F5:1 E5:.5 C5:.5 A4:1 r:1'}),57,.75),electric=reply('electric',EXP_REPLY,44,.8),bass=low(transform(ADMIN_LOW,replacement={0:'G2:1 B2:.5 E3:.5 F3:1 r:1',4:'E3:1 C3:.5 Bb2:.5 G2:1 r:1'}),44)),
 S('等待 · 开锁之前','33–40 希望未完成的半句嵌入侵蚀结尾，E属关系保留。',piano=lead('piano',cat(cut(ADMIN_B,0,4),cut(transform(ADMIN_A,replacement={7:'D#5:1 F#5:.5 B4:.5 r:2'}),4,8)),61),cello=harm('cello',A_H,'breath',36,.37),bass=low(ADMIN_LOW,41))])
def boss():
 return score(CUES['boss'],[
 S('裂口 · A','1–8 抵抗的四度被侵蚀半音打断，鼓保持切分骨架。',piano=lead('piano',BOSS_A,80),nylon=harm('nylon',BAT_H,'offbeat',58,.75),ebass=low(BOSS_LOW,64,'ebass',.66),drums=drum('drive')),
 S('入侵 · 反题','9–16 电钢提出完整侵蚀主题；撤钢琴和拨弦避免密度堆积。',electric=lead('electric',INTRUSION,68,.9),strings=harm('strings',EXP_H,'breath',44,.35),ebass=low(LAB_LOW,61,'ebass',.66),drums=drum('backbeat')),
 S('盾面 · B','17–24 木管宽线条抵消碎拍，低音转回D并向高处连接。',clarinet=lead('clarinet',BOSS_B,73,.74),nylon=harm('nylon',BAT_H,'dialogue',55,.75),ebass=low(BAT_BB,59,'ebass',.66),drums=drum()),
 S('余震 · B′','25–32 钢琴改变B的高潮与收尾；鼓退出，张力留在和声。',piano=lead('piano',transform(BOSS_B,replacement={2:'D6:1 Bb5:.5 A5:.5 F5:1 r:1',4:'C6:1 D6:.5 C6:.5 A5:1 r:1',7:'C#5:1 E5:.5 G5:.5 A4:1 r:1'}),75),cello=harm('cello',BAT_H,'held',42,.38),bass=low(HOME_BASS,54)),
 S('应答 · 希望陈述','33–40 抵抗主题首次不受半音打断，木管为其保留呼吸。',clarinet=lead('clarinet',RESOLVE,75,.74),nylon=harm('nylon',BAT_H,'pulse',57,.75),ebass=low(BAT_BASS,63,'ebass',.66),drums=drum('backbeat')),
 S('缝合 · 交错发展','41–48 四小节A与侵蚀回答交接；改变和声而非整首加速。',piano=lead('piano',cat(cut(BOSS_A,0,4),cut(transform(INTRUSION,replacement={7:'F5:.5 E5:.5 C#5:1 A4:1 r:1'}),4,8)),79),strings=harm('strings',BAT_H,'breath',46,.35),ebass=low(BOSS_LOW,64,'ebass',.66),drums=drum('drive')),
 S('A′ · 收紧阵线','49–56 A回归将半音句改成上行抵抗，末句留属。',piano=lead('piano',transform(BOSS_A,replacement={1:'C5:.5 D5:.5 F5:1 A5:.5 G5:.5 r:1',4:'A5:.5 C6:1 D6:.5 C6:.5 A5:.5 G5:.5 r:.5',5:'F5:1 D5:.5 Bb4:.5 G5:1 r:1'}),83),nylon=harm('nylon',BAT_H,'offbeat',57,.75),ebass=low(BOSS_LOW,64,'ebass',.66),drums=drum('backbeat')),
 S('破口尚在 · 接续','57–64 木管B降八度回顾，最后A属通往下一轮。',clarinet=lead('clarinet',transform(BOSS_B,octave=-1,replacement={3:'E5:1 C#5:1 A4:.5 r:1.5',7:'E5:1 C#5:.5 A4:.5 G4:.5 r:1.5'}),68,.74),nylon=harm('nylon',BAT_H,'breath',49,.75),ebass=low(BAT_BB,57,'ebass',.66),drums=drum())])
def final():
 return score(CUES['final'],[
 S('誓言 · A','1–8 抵抗主题的新陈述；钢琴保留可识别四度与附点。',piano=lead('piano',FIN_A,81),strings=harm('strings',BAT_H,'breath',46,.35),ebass=low(BAT_BASS,65,'ebass',.65),drums=drum('backbeat')),
 S('壁垒 · AI','9–16 电钢侵蚀线条与独立低音，弦乐退出。',electric=lead('electric',LAB_A,68,.8),pizz=harm('pizz',L_H,'offbeat',52,.55),ebass=low(LAB_LOW,61,'ebass',.65),drums=drum('drive')),
 S('记得谁 · 校园','17–24 校园主题完整出现，减鼓为人物留空间。',clarinet=lead('clarinet',CAMPUS,67,.73),nylon=harm('nylon',HOME_H1,'dialogue',51,.65),bass=low(SEN_LOW,53)),
 S('选择 · B','25–32 钢琴独立长线向高处展开，低音重新加入律动。',piano=lead('piano',FIN_B,79),strings=harm('strings',BAT_H,'held',44,.35),ebass=low(BAT_BB,61,'ebass',.65),drums=drum()),
 S('替补入场 · 对话','33–40 抵抗短句与校园尾句在同一段接棒，不让全员齐奏。',clarinet=lead('clarinet',cat(cut(RESOLVE,0,4),cut(transform(CAMPUS,replacement={7:'D5:1 F5:.5 E5:.5 C#5:1 r:1'}),4,8)),70,.73),piano=reply('piano',HOME_REPLY,53),ebass=low(BAT_BASS,58,'ebass',.65),drums=drum('brush')),
 S('静点 · 残存的人','41–48 校园前半化为钢琴低声，侵蚀尾句被改写为D属。',piano=lead('piano',cat(cut(SEN_A,0,4),cut(transform(INTRUSION,replacement={4:'Bb4:1 D5:.5 F5:.5 E5:1 r:1',5:'G5:1 F5:.5 E5:.5 D5:1 r:1',6:'Bb4:1 A4:.5 G4:.5 E5:1 r:1',7:'C#5:1 E5:.5 A4:.5 r:2'}),4,8)),68),cello=harm('cello',BAT_H,'breath',39,.37),bass=low(GARDEN_LOW,48)),
 S('我们仍能 · A′','49–56 原四度动机扩展到最高点，低音逆向保留地面感。',piano=lead('piano',transform(FIN_A,replacement={2:'A5:.5 C6:1 D6:.5 C6:.5 A5:.5 G5:.5 r:.5',4:'D6:1 C6:.5 A5:.5 G5:.5 F5:.5 E5:.5 r:.5',7:'A5:1 G5:.5 E5:.5 C#5:1 r:1'}),84),strings=harm('strings',BAT_H,'breath',47,.35),ebass=low(BOSS_LOW,65,'ebass',.65),drums=drum('drive')),
 S('共同的名字 · 综合','57–64 长笛前半校园、后半希望；不是互不相关的新曲。',flute=lead('flute',cat(cut(transform(CAMPUS,replacement={0:'D5:1 F5:.5 A5:.5 G5:1 r:1'}),0,4),cut(RESOLVE,4,8)),70,.64),nylon=harm('nylon',HOME_H1,'offbeat',55,.65),ebass=low(BAT_BB,61,'ebass',.65),drums=drum('backbeat')),
 S('继续选择 · 循环属段','65–72 B由木管降区回望，最后两句明确回到A属。',clarinet=lead('clarinet',transform(FIN_B,octave=-1,replacement={4:'A5:1 F5:.5 E5:.5 D5:1 r:1',6:'G5:1 F5:.5 E5:.5 C#5:1 r:1',7:'E5:1 C#5:.5 A4:.5 r:2'}),66,.73),nylon=harm('nylon',BAT_H,'dialogue',50,.65),ebass=low(BAT_BB,56,'ebass',.65),drums=drum())])
def suspense():
 return score(CUES['suspense'],[
 S('删去 · 缺席','1–8 电钢留出句中空白，pad低密度支持，不用连续低音轰鸣。',electric=lead('electric',SUS_A,49,.75),pad=harm('pad',L_H,'breath',33,.25),bass=low(LIB_LOW,36)),
 S('残页 · 新问题','9–16 低区单簧管提出独立轮廓，维持不确定的落点。',clarinet=lead('clarinet',SUS_B,47,.68),electric=reply('electric',EXP_REPLY,39,.75),bass=low(ADMIN_LOW,37)),
 S('痕迹 · 纹理生长','17–24 电钢弱拍重排，气氛层升高转位；不是只改变音量。',electric=lead('electric',transform(SUS_A,replacement={0:'r:1 E5:.5 F5:.5 Bb4:.5 r:1.5',2:'G5:1 F5:.5 E5:.5 r:2',4:'Bb4:.5 E5:.5 F5:1 r:1 B4:.5 r:.5',6:'F5:.5 E5:.5 D#5:1 B4:.5 r:1.5'}),51,.75),pad=harm('pad',A_H,'held',34,.25),bass=low(transform(LIB_LOW,replacement={2:'E3:1 C3:.5 G2:.5 r:2',5:'F3:1 D3:.5 A2:.5 r:2'}),38)),
 S('没有落款 · 回环','25–32 木管低区回归带新尾句，B属引向E；没有淡出。',clarinet=lead('clarinet',transform(SUS_B,octave=-1,replacement={1:'D5:1 B4:.5 A4:.5 r:2',4:'F5:1 E5:1 r:2',7:'D#5:1 B4:.5 F#4:.5 r:2'}),49,.68),pad=harm('pad',L_H,'breath',32,.25),bass=low(LIB_LOW,36))])
def ending():
 return score(CUES['ending'],[
 S('废墟 · 记得','1–8 钢琴恢复校园轮廓，留住原本的小调颜色。',piano=lead('piano',END_A,63),cello=harm('cello',HOME_H1,'breath',37,.35),bass=low(GARDEN_LOW,41)),
 S('同伴 · 回答','9–16 单簧管将校园后半续写，钢琴只给空隙回答。',clarinet=lead('clarinet',transform(END_A,replacement={1:'G5:1 E5:.5 C5:.5 A4:1 r:1',4:'A5:1 C6:.5 A5:.5 G5:1 r:1',7:'D5:1 F#5:.5 E5:.5 C#5:1 r:1'}),52,.72),piano=reply('piano',HOME_REPLY,46),bass=low(SEN_LOW,42)),
 S('清晨 · 希望转为大调','17–24 抵抗四度不再紧绷，以F#改变主题明暗而保持节奏身份。',piano=lead('piano',END_B,68),strings=harm('strings',END_H,'held',39,.35),bass=low(END_LOW,45)),
 S('风 · 交接','25–32 长笛接过新主题，尾句落在共同音A，竖琴分两次呼吸。',flute=lead('flute',transform(END_B,replacement={2:'A5:1 G5:.5 F#5:.5 E5:1 r:1',5:'B5:1 A5:.5 F#5:.5 E5:1 r:1',7:'E5:1 C#5:.5 A4:.5 r:2'}),53,.62),harp=harm('harp',END_H,'dialogue',43,.6),bass=low(END_LOW,43)),
 S('风云录 · 校园回收','33–40 校园主题改写F#与B自然音，在同一首中完成记忆变化。',piano=lead('piano','D5:1 A4:.5 C#5:.5 F#5:1 E5:.5 r:.5 | D5:1.5 C#5:.5 A4:1 r:1 | B4:.5 D5:.5 G5:1 F#5:.5 E5:.5 D5:1 | C#5:2 A4:1 r:1 | F#5:.75 G5:.25 A5:1 G5:.5 F#5:.5 E5:1 | D5:1 F#5:.5 E5:.5 C#5:1 r:1 | B4:1 A4:.5 G4:.5 A4:1 C#5:.5 E5:.5 | D5:2 A4:1 r:1',69),strings=harm('strings',END_H,'breath',40,.35),bass=low(END_LOW,45)),
 S('仍有故事 · 共同音返回','41–48 木管退回中音，F自然音作为借用和弦，引回最初校园记忆。',clarinet=lead('clarinet',transform(END_A,replacement={0:'D5:1 A4:1 F5:.5 r:1.5',2:'Bb4:1 D5:1 G5:.5 r:1.5',4:'F5:1 A5:1 G5:.5 r:1.5',7:'C#5:1 E5:.5 A4:.5 r:2'}),50,.72),harp=harm('harp',HOME_H1,'breath',40,.6),bass=low(GARDEN_LOW,40))])
def summon():
 return score(CUES['summon'],[
 S('点名 · A','1–8 星点是竖琴旋律，钢琴保持留拍，不用廉价全频闪光。',harp=lead('harp',SUM_A,69,.9),piano=harm('piano',HOME_H2,'breath',50,.95),bass=low(CANT_LOW,47)),
 S('信笺 · 校园','9–16 单簧管校园变奏，竖琴退出以保留音色层次。',clarinet=lead('clarinet',transform(CAMPUS,replacement={1:'D5:1 C5:.5 A4:.5 G4:1 r:1',5:'D5:1 F5:.5 A5:.5 G5:1 r:1',7:'C#5:1 E5:.5 G5:.5 A4:1 r:1'}),58,.73),piano=harm('piano',HOME_H1,'dialogue',47,.95),bass=low(Y_LOW,45)),
 S('群星 · B','17–24 钢琴展开宽阔新句，弦乐支持高点但无鼓。',piano=lead('piano',SUM_B,75,.95),strings=harm('strings',BAT_H,'breath',42,.35),bass=low(BAT_BB,51)),
 S('伙伴走来 · 回答','25–32 希望主题片段与校园尾句拼成问答，竖琴回应。',clarinet=lead('clarinet',cat(cut(RESOLVE,0,4),cut(transform(CAMPUS,replacement={7:'D5:1 F5:.5 E5:.5 C#5:1 r:1'}),4,8)),62,.73),harp=reply('harp',HOME_REPLY,49,.9),bass=low(HOME_BASS,47)),
 S('下一封信 · A′','33–40 竖琴回归扩展高点而收敛结尾，A属回到F/D。',harp=lead('harp',transform(SUM_A,replacement={1:'G5:1 A5:.5 C6:.5 B5:1 r:1',4:'E5:1 G5:.5 C6:.5 A5:1 r:1',7:'C#5:1 E5:.5 A4:.5 r:2'}),67,.9),piano=harm('piano',HOME_H2,'dialogue',46,.95),bass=low(CANT_LOW,44))])

def stingers():
 cues={c['id']:c for c in __import__('json').loads((ROOT/'music/cues.json').read_text())['stingers']}
 def save(id,bpm,voices):
  return score(dict(cues[id],bpm=bpm,lufs=-19),[S('触发与落点','从主题短动机提炼；完整终止与自然采样尾音，独立于BGM。',**voices)],loop=False)
 save('victory',112,dict(piano=lead('piano','A4:.5 D5:1 F5:.5 E5:.5 D5:.5 r:1 | Bb4:.5 D5:.5 F5:1 E5:.5 C#5:.5 A4:1 | D5+F5+A5:2 r:2',78),nylon=harm('nylon',['F3 A3 D4 F4','E3 G3 A3 C#4','F3 A3 D4 F4'],'breath',51,.7),bass=low('D3:1 A2:1 F3:1 r:1 | A2:1 E3:.5 C#3:.5 G2:1 r:1 | D2:2 r:2',57)))
 save('defeat',76,dict(piano=lead('piano','D5:1 A4:.5 C5:.5 F5:1 E5:.5 r:.5 | D5:1 C5:.5 A4:.5 G4:1 r:1 | F4+A4+D5:2 r:2',59),cello=harm('cello',['F3 A3 D4 E4','E3 G3 A3 C4','F3 A3 D4 F4'],'breath',37,.35),bass=low('D3:1 A2:1 C3:1 r:1 | C3:1 A2:1 G2:1 r:1 | D2:2 r:2',41)))
 save('rare',108,dict(harp=lead('harp','A4:.5 D5:.5 F5:.5 A5:.5 C6:1 A5:1 | G5:.5 F5:.5 E5:1 C#5:.5 E5:.5 A5:1 | D5+F5+A5:1 r:1 D6:1 r:1 | r:4',78),piano=harm('piano',['F3 A3 D4 F4','E3 G3 A3 C#4','F3 A3 D4 F4','r'],'held',61),bass=low('D3:1 F3:.5 A3:.5 C3:1 r:1 | A2:1 E3:.5 G3:.5 C#3:1 r:1 | D2:2 r:2 | r:4',53)))
 save('recruit',104,dict(nylon=lead('nylon','D5:1 A4:.5 C5:.5 F5:1 r:1 | E5:.5 D5:.5 C5:1 A4:.5 C5:.5 D5:1 | F4+A4+D5:2 r:2',73),piano=harm('piano',['F3 A3 D4 E4','E3 G3 A3 C#4','F3 A3 D4 F4'],'breath',49),bass=low('D3:1 A2:1 F3:.5 E3:.5 r:1 | A2:1 E3:.5 C#3:.5 G2:1 r:1 | D2:2 r:2',46)))
 save('chapter-clear',96,dict(piano=lead('piano','A4:.5 D5:1.5 F5:.5 E5:.5 D5:.5 r:.5 | C5:.75 D5:.25 A4:1 C5:.5 D5:1 r:.5 | F5:.5 A5:1 G5:.5 E5:.5 C#5:.5 A4:1 | D5+F#5+A5:2 r:2',77),strings=harm('strings',['F3 A3 D4 F4','E3 A3 C4 E4','E3 G3 A3 C#4','F#3 A3 D4 F#4'],'held',44,.35),bass=low('D3:1 A2:.5 C3:.5 F3:1 r:1 | C3:1 E3:.5 A2:.5 G2:1 r:1 | A2:1 E3:.5 G3:.5 C#3:1 r:1 | D2:2 r:2',54)))
 save('revelation',92,dict(electric=lead('electric','E5:.5 F5:.5 r:.5 Bb4:.5 E5:1 r:1 | D#5:.5 E5:1 B4:.5 F4:1 r:1 | E4+B4:1 r:3',62,.8),pad=harm('pad',['G3 B3 E4 F4','F#3 A3 B3 D#4','G3 B3 E4 G4'],'breath',35,.3),bass=low('E2:1 r:1 B2:.5 r:1.5 | D#3:1 B2:1 F#2:.5 r:1.5 | E2:1 r:3',45)))

if __name__=='__main__':
 for fn in [title,yifu,basketball,garden,library,canteen,playground,junior,senior,laboratory,admin,boss,final,suspense,ending,summon]:
  s=fn();print(s['id'],s['length_beats']//4,'authored bars')
 stingers()
