#!/usr/bin/env bash

# 1) Install (if you pass "setup")
if [[ $1 == "setup" ]]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  exit 0
fi

# 2) Render scenes
source .venv/bin/activate
manim -ql scenes/fall_with_tension.py TensionDocumentary

# 3) Copy result for GitHub Pages
VIDEO_PATH="media/videos/scenes/fall_with_tension/480p15/TensionDocumentary.mp4"
if [ -f "$VIDEO_PATH" ]; then
  mkdir -p docs/videos
  cp "$VIDEO_PATH" docs/videos/
fi
