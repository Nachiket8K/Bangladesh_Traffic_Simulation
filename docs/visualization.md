---
title: Visualization
nav_order: 6
---

# Visualization (Interactive)

Open the interactive demo:

Visit docs/visualization/ through a local web server to see the truck playback.

## Generate fresh playback data

The visualization is backed by exported simulation output from the Lab 4 model.

From the repository root, regenerate the playback files with:

```bash
.venv_fresh\Scripts\python.exe "Lab 4\EPA1352-G17-A4\model\export_visualization.py"
```

This writes updated files into `docs/visualization/data/`.

## What you can do
- Pick **baseline** vs **bridge-down** scenarios
- Play/pause and change speed
- See bridge state (up/down) and how delays emerge

## Data files used by the visualization
The demo reads precomputed files from `docs/visualization/data/`:

- `network.geojson`
- `bridges.geojson` (optional)
- `scenarios.json`
- `traj_*.json` (one per scenario)
