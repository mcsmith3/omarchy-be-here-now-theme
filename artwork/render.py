"""Render original Be Here Now inspired vector wallpapers with librsvg."""
from pathlib import Path
import math
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
W, H = 1800, 1200

def grain(color, opacity, seed):
    rng = random.Random(seed)
    dots = ''.join(f'<circle cx="{rng.uniform(0,W):.1f}" cy="{rng.uniform(0,H):.1f}" r="{rng.uniform(.25,.85):.2f}"/>' for _ in range(16000))
    return f'<g fill="{color}" opacity="{opacity}">{dots}</g>'

def chair(x, y, scale, color):
    # A simple wooden ladder-back chair in three-quarter perspective.
    return f'''<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">
      <path d="M-49 12 L-49 -100 Q-49 -105 -44 -104 L25 -86 Q30 -85 30 -79 L30 28"/>
      <path d="M-43 9 L-43 -96 L24 -78 L24 23 M-48 -73 L29 -53 M-48 -67 L29 -47 M-48 -39 L29 -19 M-48 -33 L29 -13"/>
      <path d="M-49 10 L29 30 L65 6 L-9 -12 Z M-49 10 L-49 18 L29 39 L65 15 L65 6 M29 30 L29 39"/>
      <path d="M-48 18 L-51 94 L-44 96 L-38 21 M27 39 L28 117 L35 114 L37 34 M58 19 L63 87 L69 83 L65 15 M-9 -10 L-6 72 L0 74 L1 -8"/>
      <path d="M-47 67 L28 89 M35 83 L63 63 M-40 62 L-5 45"/>
      <path stroke-width=".65" opacity=".6" d="M-36 12 L27 29 M-25 8 L37 24 M-14 3 L47 18 M-38 -92 L18 -77 M-40 -70 L20 -54"/>
    </g>'''

def label(text, x, y, size, color, spacing=4):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Liberation Serif,serif" font-size="{size}" letter-spacing="{spacing}" fill="{color}">{text}</text>'

def render(name, base, contents, texture_color, texture_opacity):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2560" viewBox="0 0 {W} {H}">
    <defs><radialGradient id="field"><stop stop-color="{base[0]}"/><stop offset="1" stop-color="{base[1]}"/></radialGradient></defs>
    <rect width="1800" height="1200" fill="url(#field)"/>
    {grain(texture_color,texture_opacity,42)}{contents}</svg>'''
    source = ROOT / 'artwork' / f'{name}.svg'
    source.write_text(svg)
    subprocess.run(['rsvg-convert',str(source),'-o',str(ROOT/'backgrounds'/f'{name}.png')],check=True)

# A quiet desktop: a small, warm drawing held in a wide field of violet ink.
minimal = '<circle cx="900" cy="585" r="164" stroke="#B49AD8" opacity=".17" stroke-width=".65" fill="none"/>'
minimal += chair(900,585,.88,'#D7C5A4')
minimal += label('B E   H E R E   N O W',900,840,12,'#B7A38C',2)
render('01-chair',('#291F35','#17121F'),minimal,'#D6C4E0',.075)

# A new radial construction; the center remains clear for the empty chair.
cx, cy, r = 900, 595, 290
geometry = []
for i in range(72):
    a = 2*math.pi*i/72
    b = a + 2*math.pi*24/72
    geometry.append(f'<path d="M{cx+r*math.cos(a):.3f},{cy+r*math.sin(a):.3f} L{cx+r*math.cos(b):.3f},{cy+r*math.sin(b):.3f}"/>')
mandala = '<g fill="none" stroke="#E4D4B7" stroke-width=".72" opacity=".48">'+''.join(geometry)+'</g>'
for radius, opacity, width in [(147,.5,.8),(290,.8,1),(298,.5,.7),(360,.5,.7),(366,.25,.6)]:
    mandala += f'<circle cx="900" cy="595" r="{radius}" fill="none" stroke="#E4D4B7" opacity="{opacity}" stroke-width="{width}"/>'
for rotation in range(0,360,90):
    # Individual glyphs follow the circle, avoiding renderer-dependent text paths.
    text='BE HERE NOW'
    for i,char in enumerate(text):
        angle=rotation+(i-(len(text)-1)/2)*4.7
        mandala += f'<g transform="rotate({angle} 900 595)">'+label(char,900,268,22,'#E4D4B7',0)+'</g>'
    mandala += f'<g transform="rotate({rotation+45} 900 595)"><path d="M900 259 l4 6 -4 6 -4 -6 Z" fill="#DDB568" opacity=".8"/></g>'
mandala += chair(900,583,.86,'#E4D4B7')
mandala += label('R E M E M B E R',900,145,17,'#DDB568',3)
mandala += label('B E   H E R E   N O W',900,1060,14,'#CDBBDA',2)
render('02-mandala',('#4A3664','#281E3C'),mandala,'#E4D4B7',.1)

# Brown-paper print: original lotus linework and a restrained sunburst.
lotus = '<g stroke="#60432F" fill="none" stroke-linecap="round" stroke-linejoin="round">'
for i in range(64):
    a=2*math.pi*i/64
    r1=225 if i%4 else 218
    r2=234 if i%4 else 244
    lotus += f'<path opacity=".45" stroke-width=".85" d="M{900+r1*math.cos(a):.2f} {560+r1*math.sin(a):.2f} L{900+r2*math.cos(a):.2f} {560+r2*math.sin(a):.2f}"/>'
lotus += '<circle cx="900" cy="560" r="210" opacity=".35" stroke-width=".8"/>'
lotus += '''<g transform="translate(900 600)" stroke-width="1.7">
<path d="M0 55 C-70 4 -53 -83 0 -150 C53 -83 70 4 0 55Z"/>
<path d="M0 55 C-103 44 -135 -24 -129 -99 C-48 -74 2 -28 0 55Z M0 55 C103 44 135 -24 129 -99 C48 -74 -2 -28 0 55Z"/>
<path d="M0 55 C-104 102 -183 42 -201 -15 C-112 -35 -42 -5 0 55Z M0 55 C104 102 183 42 201 -15 C112 -35 42 -5 0 55Z"/>
<path d="M0 55 C-70 111 -127 102 -163 79 C-109 49 -56 42 0 55Z M0 55 C70 111 127 102 163 79 C109 49 56 42 0 55Z"/>
<path opacity=".5" stroke-width=".8" d="M0 42 L0 -126 M-12 45 Q-60 -4 -115 -79 M12 45 Q60 -4 115 -79 M-22 55 Q-96 20 -179 -7 M22 55 Q96 20 179 -7"/>
</g></g>'''
lotus += label('BE HERE NOW',900,887,34,'#60432F',7)
lotus += '<path d="M864 928 H936" stroke="#60432F" stroke-width=".8" opacity=".5"/>'
lotus += label('REMEMBER',900,967,12,'#78573B',5)
render('03-brown-paper',('#D3B88D','#B59569'),lotus,'#513525',.16)
# Indigo cover-style print: a chord-web sphere around a large empty chair,
# with ring lettering and REMEMBER on four sides.
cx, cy, r = 900, 600, 318
points = 24
web = ['<g fill="none" stroke="#F4F1FF" stroke-width="1.5" stroke-linecap="round">']
for step in (5, 7, 9):
    for i in range(points):
        a = 2*math.pi*i/points - math.pi/2
        b = a + 2*math.pi*step/points
        web.append(f'<path d="M{cx+r*math.cos(a):.3f},{cy+r*math.sin(a):.3f} L{cx+r*math.cos(b):.3f},{cy+r*math.sin(b):.3f}"/>')
web.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-width="2.2"/></g>')
remember = ''.join(web)
# Knock the web back behind the chair so its outline reads clearly.
remember += f'<ellipse cx="{cx+4}" cy="{cy+8}" rx="98" ry="212" fill="#3A2F98" opacity=".55"/>'
woven = ''.join(f'<path d="M{-47+i*7.5:.1f} {11+i*2:.1f} L{-11+i*7.5:.1f} {-10+i*2:.1f}"/>' for i in range(10))
remember += f'''<g transform="translate({cx} {cy+18}) scale(1.95)" fill="none" stroke="#F4F1FF" stroke-width=".55" opacity=".85">{woven}</g>'''
remember += chair(cx, cy+18, 1.95, '#F4F1FF').replace('stroke-width="2"', 'stroke-width="1.35"', 1)
ring = 'BE HERE NOW ' * 7
for i, char in enumerate(ring):
    if char == ' ':
        continue
    angle = 360*i/len(ring)
    remember += f'<g transform="rotate({angle:.3f} {cx} {cy})">' + label(char, cx, cy-r-14, 36, '#F4F1FF', 0) + '</g>'
for rotation in (0, 90, 180, 270):
    remember += f'<g transform="rotate({rotation} {cx} {cy})">' + label('REMEMBER', cx, cy-r-96, 40, '#F4F1FF', 3) + '</g>'
render('00-remember', ('#4A3DB2', '#2C237E'), remember, '#F4F1FF', .07)
print('Rendered four 3840 × 2560 wallpapers.')


# Long-exposure "still point": one person stands still, sharp, while a blurred,
# multiple-exposure crowd streams past on every side of a station hall.
def walker(x, y, s, phase, color, bag=False):
    """A walking silhouette with its feet at (x, y); phase sets the stride."""
    sw = math.sin(phase)
    g = [f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" fill="{color}" stroke="{color}" '
         'stroke-linecap="round" stroke-linejoin="round">',
         '<ellipse cx="0" cy="-160" rx="10" ry="12" stroke="none"/>',
         '<path d="M-14 -142 Q-21 -140 -21 -128 L-18 -72 L18 -72 L21 -128 Q21 -140 14 -142 Z" stroke-width="2"/>',
         f'<path d="M-6 -76 L{-6+20*sw:.1f} -38 L{-5+28*sw:.1f} -2" fill="none" stroke-width="10"/>',
         f'<path d="M6 -76 L{6-20*sw:.1f} -38 L{5-28*sw:.1f} -2" fill="none" stroke-width="10"/>',
         f'<path d="M-21 -132 L{-23-14*sw:.1f} -104 L{-21-20*sw:.1f} -80" fill="none" stroke-width="7"/>',
         f'<path d="M21 -132 L{23+14*sw:.1f} -104 L{21+20*sw:.1f} -80" fill="none" stroke-width="7"/>']
    if bag:
        g.append(f'<rect x="{18+20*sw:.1f}" y="-92" width="16" height="22" rx="3" stroke="none"/>')
    g.append('</g>')
    return ''.join(g)

rng = random.Random(23)
horizon, cx = 560, 900
still = ['<defs>']
for i in range(8):
    still.append(f'<filter id="motion{i}" x="-60%" y="-10%" width="220%" height="120%">'
                 f'<feGaussianBlur stdDeviation="{2+i*2.2:.1f} .5"/></filter>')
still.append('<filter id="trail" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="8 1.4"/></filter>'
             '<filter id="soft"><feGaussianBlur stdDeviation="4"/></filter>'
             '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>'
             '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0F0C16"/>'
             f'<stop offset="1" stop-color="#2C2140"/></linearGradient>'
             '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#30243F"/>'
             '<stop offset="1" stop-color="#110D17"/></linearGradient></defs>')
still.append(f'<rect width="{W}" height="{horizon}" fill="url(#sky)"/>')
still.append(f'<rect y="{horizon}" width="{W}" height="{H-horizon}" fill="url(#ground)"/>')
# Hall: a far wall of arches and a floor whose seams run to one vanishing point.
hall = ['<g fill="none" stroke="#B49AD8" stroke-width="1" opacity=".14">']
for x in range(-40, W+80, 160):
    hall.append(f'<path d="M{x} {horizon} V250 A80 80 0 0 1 {x+160} 250 V{horizon}"/>')
for i in range(-14, 15):
    hall.append(f'<path d="M{cx} {horizon} L{cx+i*170} {H}" opacity=".7"/>')
for y in (590, 630, 690, 780, 910, 1090):
    hall.append(f'<path d="M0 {y} H{W}" opacity=".5"/>')
hall.append(f'<path d="M0 {horizon} H{W}" stroke="#DDB568" opacity=".5"/></g>')
still += hall
still.append(f'<ellipse cx="{cx}" cy="{horizon+120}" rx="420" ry="260" fill="#DDB568" opacity=".1" filter="url(#glow)"/>')

def trails(count, y0, y1, alpha):
    out = []
    for _ in range(count):
        y = rng.uniform(y0, y1)
        x0 = rng.uniform(-300, W)
        length = rng.uniform(300, 1200)
        color = rng.choice(('#DDB568', '#DFA070', '#EBC986', '#92B8B0', '#CFB3EF', '#DDB568'))
        out.append(f'<path d="M{x0:.0f} {y:.1f} H{x0+length:.0f}" stroke="{color}" stroke-width="{rng.uniform(1,2.4):.1f}" '
                   f'opacity="{rng.uniform(*alpha):.2f}" stroke-linecap="round" filter="url(#trail)"/>')
    return out

still += trails(18, horizon-140, horizon+60, (.2, .5))
# The crowd: feet lower on the floor means nearer, larger, and more blurred.
figure_y, figure_s = 930, 2.3
people = []
for _ in range(40):
    y = horizon + 30 + (H + 60 - horizon - 30) * rng.random() ** 1.3
    t = (y - horizon) / (H - horizon)
    s = 0.45 + t * 2.1
    x = rng.uniform(-150, W + 150)
    if y > figure_y and abs(x - cx) < 260 and rng.random() < .7:
        x += rng.choice((-1, 1)) * 420
    if abs(x - cx) < 60 * s and abs(y - figure_y) < 90:
        continue
    people.append((y, x, s))
people.sort()
crowd_back, crowd_front = [], []
for y, x, s in people:
    blur = min(7, int(s * 2.4))
    direction = rng.choice((-1, 1))
    color = rng.choice(('#9B8AA6', '#B49AD8', '#8A79A3', '#CDBBDA', '#A898BE'))
    spacing = rng.uniform(26, 44) * s
    front = y > figure_y
    base = (.46 - .1 * t) if not front else .2
    group = [f'<g filter="url(#motion{blur})">']
    for k in range(5):
        group.append(f'<g opacity="{base*(0.62**k):.3f}">'
                     + walker(x - direction*k*spacing, y, s, rng.uniform(0, 6.3), color, rng.random() < .25) + '</g>')
    group.append('</g>')
    (crowd_front if front else crowd_back).append(''.join(group))
still.append(f'<g transform="translate(0 {2*figure_y}) scale(1 -1)" opacity=".08">' + ''.join(crowd_back[-12:]) + '</g>')
still += crowd_back
# The one who stands still: sharp, upright, rimmed in saffron light.
r = 1.6 / figure_s
still.append(f'<ellipse cx="{cx}" cy="{figure_y}" rx="{34*figure_s:.0f}" ry="{6*figure_s:.0f}" fill="#0B0910" opacity=".6" filter="url(#soft)"/>')
still.append(f'<ellipse cx="{cx}" cy="{figure_y-90*figure_s:.0f}" rx="{60*figure_s:.0f}" ry="{110*figure_s:.0f}" fill="#DDB568" opacity=".16" filter="url(#glow)"/>')
still.append(f'''<g transform="translate({cx} {figure_y}) scale({figure_s})" fill="#141019" stroke="#DDB568" stroke-width="{r:.2f}" stroke-linejoin="round">
  <path d="M-10 -66 L-10.5 -5 L-3 -5 L-1 -66 Z"/>
  <path d="M1 -66 L3 -5 L10.5 -5 L10 -66 Z"/>
  <path d="M-12.5 -5 Q-13 0 -7 0 L-2 0 L-2.5 -5 Z M12.5 -5 Q13 0 7 0 L2 0 L2.5 -5 Z"/>
  <path d="M-21 -133 Q-26 -110 -25 -86 L-20.5 -86 Q-20.5 -108 -16 -127 Z"/>
  <path d="M21 -133 Q26 -110 25 -86 L20.5 -86 Q20.5 -108 16 -127 Z"/>
  <ellipse cx="-22.8" cy="-83" rx="2.6" ry="3.4"/><ellipse cx="22.8" cy="-83" rx="2.6" ry="3.4"/>
  <path d="M-14 -144 Q-21 -142 -22 -130 L-19 -100 L-18.5 -64 L18.5 -64 L19 -100 L22 -130 Q21 -142 14 -144 Z"/>
  <path d="M-4 -153 L-4 -143 L4 -143 L4 -153 Z"/>
  <ellipse cx="0" cy="-164" rx="9.5" ry="11.5"/>
</g>''')
still += crowd_front
still += trails(8, figure_y + 40, H, (.12, .3))
render('07-still-point', ('#1A1424', '#1A1424'), ''.join(still), '#E4D4B7', .06)
print('Rendered the long-exposure wallpaper.')
