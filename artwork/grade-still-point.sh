#!/usr/bin/env bash
# Rebuild backgrounds/07-still-point.png from the source photo.
# Source: "Long-exposure crowds" by Colin Knowles, CC BY-SA 2.0
# https://commons.wikimedia.org/wiki/File:Long-exposure_crowds_(24410415379).jpg
# Crops to 3:2 (leaving out the parked car) and maps tones onto the theme
# palette: plum shadows, violet mids, saffron and paper highlights.
set -euo pipefail
cd "$(dirname "$0")/.."
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
curl -sL -A "omarchy-be-here-now-theme" -o "$work/source.jpg" \
  "https://upload.wikimedia.org/wikipedia/commons/f/f8/Long-exposure_crowds_%2824410415379%29.jpg"
magick -size 1x1 xc:'#0E0B14' xc:'#241A33' xc:'#4A3664' xc:'#8A6A9E' xc:'#DDB568' xc:'#F5EBD9' \
  +append -filter Cubic -resize 256x1! "$work/ramp.png"
magick "$work/source.jpg" -crop 3139x2093+1017+130 +repage -resize 2880x1920 \
  -colorspace gray -level 2%,96% "$work/ramp.png" -clut -strip backgrounds/07-still-point.png
echo "Wrote backgrounds/07-still-point.png"
