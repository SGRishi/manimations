# Manimations

This project contains Manim scenes and a simple GitHub Pages site.

## Rendering

Use the helper script to set up the environment and render the scene:

```bash
./build.sh setup     # install virtual environment and dependencies
./build.sh           # render scenes
```

Rendered videos appear under `media/videos` following Manim's default
structure. The `docs/index.html` page references these videos so they can
be viewed directly on GitHub Pages after rendering.

