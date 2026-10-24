#!/usr/bin/env bash
# Rebuild backgrounds/07-still-point.png from the source photo.
# Source: "Grand Central Station long exposure" by T meltzer, CC BY-SA 4.0
# https://commons.wikimedia.org/wiki/File:Grand_Central_Station_long_exposure.jpg
# Scales to 2880 x 1920 and maps tones onto the theme palette: plum shadows,
# violet mids, saffron and paper highlights.
set -euo pipefail
cd "$(dirname "$0")/.."
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
curl -sL -A "omarchy-be-here-now-theme" -o "$work/source.jpg" \
  "https://upload.wikimedia.org/wikipedia/commons/a/a7/Grand_Central_Station_long_exposure.jpg"
magick -size 1x1 xc:'#0E0B14' xc:'#241A33' xc:'#4A3664' xc:'#8A6A9E' xc:'#DDB568' xc:'#F5EBD9' \
  +append -filter Cubic -resize 256x1! "$work/ramp.png"
magick "$work/source.jpg" -resize 2880x1920^ -gravity center -extent 2880x1920 \
  -colorspace gray -level 4%,100%,0.75 "$work/ramp.png" -clut -strip PNG8:backgrounds/07-still-point.png
echo "Wrote backgrounds/07-still-point.png"
