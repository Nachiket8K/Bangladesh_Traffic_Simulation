---
title: Visualization
nav_order: 6
---

# Visualization (Interactive)

This project includes a **GitHub-hostable interactive viewer** under `docs/visualization/`.

<div style="display:flex; gap:12px; flex-wrap:wrap; margin:14px 0 18px 0;">
  <a class="btn btn-primary" href="{{ site.baseurl }}/visualization/">Open Hosted Visualization</a>
  <a class="btn" href="{{ site.baseurl }}/">Back to Home</a>
</div>

When this repository is published with **GitHub Pages** from the `docs/` folder, the viewer will be available at:

```text
{{ site.url }}{{ site.baseurl }}/visualization/
```

The viewer includes:
- Chittagong Port → Dhaka truck playback
- baseline and disrupted bridge scenarios
- Processed scenario ladder exports
- reset, speed control, and scenario switching

## What you can do
- Pick from **baseline** and multiple **bridge disruption** scenarios
- Play/pause and change speed
- See bridge state (up/down) and how delays emerge

## Data files used by the visualization
The demo reads precomputed files from `docs/visualization/data/`:

- `network.geojson`
- `bridges.geojson` (optional)
- `scenarios.json`
- `traj_*.json` (one per scenario)
