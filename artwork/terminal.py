"""Render 08-terminal: a terminal window with ASCII lettering and mandalas."""
from pathlib import Path
import math
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
W, H = 1800, 1200
FONT = 14
CW, CH = FONT * 0.6, FONT * 1.25          # character cell
WX, WY, WW, WH = 70, 60, 1660, 1080       # terminal window
PAD = 30
COLS = int((WW - 2 * PAD) / CW)
ROWS = int((WH - 2 * PAD) / CH)

BG, FG, MUTED = '#191421', '#EADCC3', '#9B8AA6'
SAFFRON, ORANGE, MAGENTA = '#DDB568', '#DFA070', '#B49AD8'
LAVENDER, CYAN, GREEN, PLUM = '#CFB3EF', '#92B8B0', '#A9B58D', '#49365F'
PLUM_LIGHT = '#6E5687'

grid = {}   # (row, col) -> (char, color)


def put(row, col, text, color=FG):
    for i, ch in enumerate(text):
        if ch != ' ' and 0 <= row < ROWS and 0 <= col + i < COLS:
            grid[(row, col + i)] = (ch, color)


# ANSI Shadow lettering, drawn with full blocks and box-drawing shadows.
LETTERS = {
    'B': ['██████╗ ', '██╔══██╗', '██████╔╝', '██╔══██╗', '██████╔╝', '╚═════╝ '],
    'E': ['███████╗', '██╔════╝', '█████╗  ', '██╔══╝  ', '███████╗', '╚══════╝'],
    'H': ['██╗  ██╗', '██║  ██║', '███████║', '██╔══██║', '██║  ██║', '╚═╝  ╚═╝'],
    'R': ['██████╗ ', '██╔══██╗', '██████╔╝', '██╔══██╗', '██║  ██║', '╚═╝  ╚═╝'],
    'N': ['███╗   ██╗', '████╗  ██║', '██╔██╗ ██║', '██║╚██╗██║', '██║ ╚████║', '╚═╝  ╚═══╝'],
    'O': [' ██████╗ ', '██╔═══██╗', '██║   ██║', '██║   ██║', '╚██████╔╝', ' ╚═════╝ '],
    'W': ['██╗    ██╗', '██║    ██║', '██║ █╗ ██║', '██║███╗██║', '╚███╔███╔╝', ' ╚══╝╚══╝ '],
    ' ': ['   '] * 6,
}


def banner(text):
    rows = [''] * 6
    for ch in text:
        for i in range(6):
            rows[i] += LETTERS[ch][i]
    return rows


def tangent_char(nx, ny):
    """ASCII stroke for a curve whose normal is (nx, ny) in screen space (y down)."""
    a = math.degrees(math.atan2(nx, ny)) % 180  # tangent angle, y up
    if a < 22.5 or a >= 157.5:
        return '-'
    if a < 67.5:
        return '/'
    if a < 112.5:
        return '|'
    return '\\'


def mandala(cr, cc, radius, k, palette):
    """Rings and petals; outlines use - / | \\ following the curve."""
    s = radius / 16
    aspect = CW / CH
    half = 0.42

    def lobe(th, base, tip, n, phase=0.0):
        return base + (tip - base) * abs(math.cos(n * th / 2 + phase)) ** 0.9

    layers = [  # (signed distance function, outline colour, fill char, fill colour)
        (lambda r, th: abs(r - 15.6 * s) - half, palette[0], None, None),
        (lambda r, th: r - lobe(th, 8.2 * s, 14.2 * s, k), palette[1], '.', palette[2]),
        (lambda r, th: abs(r - 7.6 * s) - half, palette[3], None, None),
        (lambda r, th: r - lobe(th, 2.6 * s, 6.6 * s, k, math.pi / 2), palette[4], ':', palette[5]),
    ]
    for dr in range(-radius - 1, radius + 2):
        for dc in range(-int(radius / aspect) - 2, int(radius / aspect) + 3):
            x, y = dc * aspect, dr
            r = math.hypot(x, y)
            if r > 16.4 * s:
                continue
            th = math.atan2(y, x)
            cell = None
            if r < 1.4 * s:
                cell = ('@' if r < 0.5 else 'o', palette[6])
            elif abs(r - 15.0 * s) < 0.6 * s and math.cos(2 * k * th) > 0.9:
                cell = ('o', palette[6])
            elif abs(r - 7.0 * s) < 0.45 and math.cos(k * th) > 0.93:
                cell = ('*', palette[6])
            else:
                for f, outline, fill, fill_color in layers:
                    d = f(r, th)
                    if abs(d) <= half if fill is None else -half * 1.6 <= d <= 0:
                        e = 0.05
                        gx = f(math.hypot(x + e, y), math.atan2(y, x + e)) - f(math.hypot(x - e, y), math.atan2(y, x - e))
                        gy = f(math.hypot(x, y + e), math.atan2(y + e, x)) - f(math.hypot(x, y - e), math.atan2(y - e, x))
                        if fill is None and abs(d) <= half:
                            gx, gy = (x, y) if gx == gy == 0 else (gx, gy)
                        cell = (tangent_char(gx, gy), outline)
                        break
                    if fill and d < 0 and (dr + dc) % 2 == 0 and r > 1.4 * s:
                        cell = (fill, fill_color)
                        break
            if cell:
                grid[(cr + dr, cc + dc)] = cell


# Prompt and command.
put(0, 0, '~/be-here-now', CYAN)
put(0, 14, '❯', SAFFRON)
put(0, 16, 'remember --here --now', FG)

# Title.
title = banner('BE HERE NOW')
tc = (COLS - len(title[0])) // 2
for i, line in enumerate(title):
    for j, ch in enumerate(line):
        if ch != ' ':
            put(3 + i, tc + j, ch, SAFFRON if ch == '█' else ORANGE)
put(10, (COLS - 41) // 2, '·  r e m e m b e r  ·  b e   h e r e  ·', MUTED)

# Mandalas: one large in the middle, two smaller at the sides.
mandala(29, COLS // 2, 16, 8, [MAGENTA, SAFFRON, PLUM_LIGHT, LAVENDER, ORANGE, MUTED, SAFFRON])
mandala(28, 26, 11, 6, [CYAN, LAVENDER, PLUM_LIGHT, SAFFRON, MAGENTA, MUTED, ORANGE])
mandala(28, COLS - 27, 11, 6, [ORANGE, MAGENTA, PLUM_LIGHT, CYAN, SAFFRON, MUTED, LAVENDER])

# A breathing meter and a fresh prompt.
base = ROWS - 8
put(base, 2, 'inhale', GREEN)
put(base, 10, '▕' + '█' * 24 + '░' * 8 + '▏', GREEN)
put(base, 46, '4s', MUTED)
put(base + 1, 2, 'hold', MAGENTA)
put(base + 1, 10, '▕' + '█' * 14 + '░' * 18 + '▏', MAGENTA)
put(base + 1, 46, '7s', MUTED)
put(base + 2, 2, 'exhale', SAFFRON)
put(base + 2, 10, '▕' + '█' * 32 + '▏', SAFFRON)
put(base + 2, 46, '8s', MUTED)
put(base + 4, 2, 'the present moment is the only moment available to us.', MUTED)
put(ROWS - 2, 0, '~/be-here-now', CYAN)
put(ROWS - 2, 14, '❯', SAFFRON)

# Box-drawing segments: which edges of the cell each character joins.
JOINS = {'═': 'EW', '║': 'NS', '╗': 'WS', '╔': 'ES', '╝': 'WN', '╚': 'EN'}


def cell_svg(row, col, ch, color):
    x = WX + PAD + col * CW
    y = WY + PAD + row * CH
    if ch == '█':
        return f'<rect x="{x:.2f}" y="{y:.2f}" width="{CW + .3:.2f}" height="{CH + .3:.2f}" fill="{color}"/>'
    if ch in JOINS:
        cx, cy, d = x + CW / 2, y + CH / 2, 1.2
        parts = []
        for side in JOINS[ch]:
            for off in (-d, d):
                if side in 'EW':
                    x2 = x + CW + .2 if side == 'E' else x - .2
                    parts.append(f'M{cx:.2f} {cy + off:.2f} H{x2:.2f}')
                else:
                    y2 = y + CH + .2 if side == 'S' else y - .2
                    parts.append(f'M{cx + off:.2f} {cy:.2f} V{y2:.2f}')
        return f'<path d="{" ".join(parts)}" stroke="{color}" stroke-width=".9" fill="none"/>'
    if ch == '░':
        return f'<rect x="{x + 1:.2f}" y="{y + 3:.2f}" width="{CW - 2:.2f}" height="{CH - 6:.2f}" fill="{color}" opacity=".25"/>'
    if ch in '▕▏':
        bx = x + CW - 1.4 if ch == '▕' else x
        return f'<rect x="{bx:.2f}" y="{y + 1:.2f}" width="1.4" height="{CH - 2:.2f}" fill="{color}" opacity=".7"/>'
    esc = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}.get(ch, ch)
    return (f'<text x="{x + CW / 2:.2f}" y="{y + CH * .78:.2f}" text-anchor="middle" '
            f'font-family="JetBrainsMono Nerd Font" font-size="{FONT}" fill="{color}">{esc}</text>')


def grain(seed):
    rng = random.Random(seed)
    dots = ''.join(f'<circle cx="{rng.uniform(0, W):.1f}" cy="{rng.uniform(0, H):.1f}" r="{rng.uniform(.25, .8):.2f}"/>'
                   for _ in range(9000))
    return f'<g fill="#D6C4E0" opacity=".05">{dots}</g>'


cursor_x = WX + PAD + 16 * CW
cursor_y = WY + PAD + (ROWS - 2) * CH
cells = ''.join(cell_svg(r, c, ch, color) for (r, c), (ch, color) in sorted(grid.items()))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2560" viewBox="0 0 {W} {H}">
<defs><radialGradient id="desk"><stop stop-color="#261D32"/><stop offset="1" stop-color="#100C16"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="url(#desk)"/>{grain(5)}
<rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" fill="{BG}" stroke="{SAFFRON}" stroke-width="2"/>
{cells}
<rect x="{cursor_x:.2f}" y="{cursor_y:.2f}" width="{CW:.2f}" height="{CH:.2f}" fill="{SAFFRON}"/>
</svg>'''
source = ROOT / 'artwork' / '08-terminal.svg'
source.write_text(svg)
subprocess.run(['rsvg-convert', str(source), '-o', str(ROOT / 'backgrounds' / '08-terminal.png')], check=True)
print(f'Rendered 08-terminal ({COLS} x {ROWS} cells).')
