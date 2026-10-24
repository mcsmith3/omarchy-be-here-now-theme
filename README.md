# Be Here Now for Omarchy

A dark [Omarchy](https://omarchy.org) theme inspired by Ram Dass's *Be Here Now*:
violet ink, warm paper, and saffron accents, with nine wallpapers:
an indigo cover-style print, chairs, mandalas, a meditating figure at a CRT
terminal, a long-exposure photo of Grand Central's main hall, and an ASCII
terminal.

![Be Here Now with fastfetch, Omanta, and two terminals](docs/screenshots/04-terminals.png)

## Screenshots

| | |
| --- | --- |
| ![Flockr with Neovim, a file tree, and a shell](docs/screenshots/01-flockr.png) | ![OmaShow editing a presentation](docs/screenshots/02-omashow.png) |
| **Flockr** with Neovim, a file tree, and a shell | **OmaShow** editing a presentation |
| ![OmaZettel with a note, outline, tags, and backlinks](docs/screenshots/03-omazettel.png) | ![fastfetch, Omanta, and two terminals](docs/screenshots/04-terminals.png) |
| **OmaZettel** with a note, outline, tags, and backlinks | **fastfetch**, **Omanta**, and two terminals |

## The look

- Deep violet base (`#191421`) with warm paper text (`#EADCC3`).
- Saffron (`#DDB568`) for the accent, cursor, and active window border.
- Plum selections (`#49365F`) that keep text readable in terminals and editors.
- Soft, warm ANSI colors: red, green, and yellow stay distinct for errors,
  success, and warnings.
- `Yaru-yellow` icons.
- Nine wallpapers and an optional pixel-dissolve screensaver.

| Role | Color |
| --- | --- |
| Background | `#191421` |
| Foreground (paper) | `#EADCC3` |
| Accent (saffron) | `#DDB568` |
| Selection (plum) | `#49365F` |
| Muted (lavender) | `#9B8AA6` |
| Magenta | `#B49AD8` |
| Green (sage) | `#A9B58D` |
| Red (clay) | `#D88978` |

The palette in `colors.toml` drives Omarchy's generated terminal, editor,
shell, and app themes. Your fonts, layout, and animation settings stay as they
are.

## Install

```sh
omarchy theme install https://github.com/mcsmith3/omarchy-be-here-now-theme
omarchy theme set be-here-now
```

To pick up changes later, run `omarchy theme update`.

## Wallpapers

![The nine wallpapers](docs/wallpapers.jpg)

| File | Description |
| --- | --- |
| `00-remember.png` | Default. Indigo print: a white chord-web sphere around an empty chair, ringed by BE HERE NOW and REMEMBER. |
| `01-chair.png` | A single hand-drawn chair on deep violet. |
| `02-mandala.png` | The chair inside a ring of type and fine line work. |
| `03-brown-paper.png` | A lotus on warm brown paper. |
| `04-cosmic-mandala.png` | An empty chair inside a large psychedelic mandala. |
| `05-lotus-pose-terminal.png` | A stick figure in lotus pose at a CRT terminal. |
| `06-lotus-terminal.png` | A lotus-shaped figure at a CRT terminal. |
| `07-still-point.png` | Long-exposure photo of Grand Central's main hall: a few people stand still while the crowd blurs past. Recoloured to the palette. |
| `08-terminal.png` | A terminal window: BE HERE NOW in ASCII block letters, three ASCII mandalas, and a breathing meter. |

Cycle through them with `omarchy theme bg next`.

`00-remember`, `01`–`03`, and `08-terminal` are 3840 × 2560 vector renders.
Their editable SVGs and the scripts that draw them are in `artwork/`. Rebuild
them with `python artwork/render.py` and `python artwork/terminal.py`. Both need
`rsvg-convert` (package `librsvg`), and the terminal also needs JetBrainsMono
Nerd Font. The other three (`04`–`06`) are 1536 × 1024 illustrations made with
an image-generation model; their full prompts are in
`artwork/psychedelic-prompts.json`.

`00-remember` is a new drawing in the spirit of the 1971 cover; none of the
drawn or generated artwork is scanned or copied from the book.

`07-still-point` is a recoloured version of
[“Grand Central Station long exposure”](https://commons.wikimedia.org/wiki/File:Grand_Central_Station_long_exposure.jpg)
by T meltzer, licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The
recoloured version is shared under the same licence.
`artwork/grade-still-point.sh` rebuilds it from the original.

## Pixel-dissolve screensaver

This is optional. The nine wallpapers take turns on screen: each one dissolves
in from coarse pixels over about three seconds, holds in full detail for twelve
seconds, then dissolves back out over deep plum before the next one arrives.

```sh
python3 "$(omarchy theme dir be-here-now)/scripts/install-screensaver.py" --check
python3 "$(omarchy theme dir be-here-now)/scripts/install-screensaver.py"
omarchy restart shell
~/.local/share/omarchy-be-here-now/launch-screensaver --preview
```

The installer copies the saver to `~/.local/share/omarchy-be-here-now/` and
routes Omarchy's idle screensaver through a small theme-aware dispatcher in
`~/.local/share/omarchy-theme-screensaver/`. While another theme is active, you
get the stock Omarchy screensaver. On first install it clones the `omarchy.idle`
plugin to point it at the dispatcher, then asks you to restart the shell. If
another theme has already set up the dispatcher, it just adds a Be Here Now
entry and no restart is needed. It backs up everything it changes to
`~/.local/state/omarchy/backups/`.

It keeps Omarchy's own idle and lock timing and the screensaver-off toggle. Any
key, mouse movement, click, or scroll dismisses it.

Set `BE_HERE_NOW_PREVIEW_SECONDS=30` to have a preview close itself after 30
seconds. Rerun the installer after you edit the screensaver or the wallpapers.
The shader is `screensaver/pixel-dissolve.frag`; rebuild it after edits with:

```sh
/usr/lib/qt6/bin/qsb --glsl '100 es,120,150' --hlsl 50 --msl 12 \
  -o screensaver/pixel-dissolve.frag.qsb screensaver/pixel-dissolve.frag
```

## Make it yours

`colors.toml` is the palette source and `icons.theme` names the icon theme.
Re-apply the theme after an edit with `omarchy theme set be-here-now`.

## License

[MIT](LICENSE), except `backgrounds/07-still-point.png`, which is
CC BY-SA 4.0 (see above). *Be Here Now* is a book by Ram Dass. This theme is a
fan tribute and is not affiliated with or endorsed by Ram Dass, the Love Serve
Remember Foundation, or the book's publishers.
