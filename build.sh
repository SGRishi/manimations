#!/usr/bin/env bash

# 1) Install (if you pass “setup”)
if [[ $1 == "setup" ]]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  exit 0
fi

# 2) Render scenes
source .venv/bin/activate
manim -pql scenes/fall_with_tension.py FallWithTension

