# Kalman Filter Visualization Scaffold

This repository is being prepared for an interactive Kalman filter
visualization. The goal is to render estimation behavior in 2D/3D using
Matplotlib for quick plots and Manim for polished animations. The codebase is
currently scaffolded so that filter algorithms, scenario generators, and
renderers can be added without reshuffling the project later.

The previous ray-tracing experiment remains in `src/raytracer/` while the new
Kalman-focused layout is built. Existing tests continue to validate the earlier
code until the new modules gain coverage.

## Quick start

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Explore the scaffolding:

   - Review `docs/architecture.md` for an overview of the planned modules.
   - Open `src/kalman_viz/` to see where configuration, filters, simulations,
     visualization adapters, and scripts will live.

3. Run the existing tests (ray-tracing code):

   ```bash
   pytest -q
   ```

## Repository layout

- `src/kalman_viz/config/` — shared configuration dataclasses and helpers.
- `src/kalman_viz/filters/` — filter interfaces and factories to plug in
  specific Kalman variants.
- `src/kalman_viz/simulations/` — synthetic scenarios and trajectory generators
  for producing measurement streams.
- `src/kalman_viz/data/` — data loaders for recorded or generated trajectories.
- `src/kalman_viz/visualization/` — rendering adapters for Matplotlib or Manim.
- `src/kalman_viz/scripts/` — CLI-friendly orchestration utilities.
- `docs/` — architecture notes and future design docs.
- `src/raytracer/` — legacy ray-tracing code kept during the transition.
- `tests/` — tests for existing functionality; new Kalman modules will be added
  here as they are implemented.

## Next steps

- Implement concrete Kalman filters and trajectory generators.
- Connect measurement loaders to CSV/parquet data.
- Flesh out Matplotlib and Manim renderers and add sample demos.
- Extend the CLI in `src/kalman_viz/scripts/visualize.py` to run end-to-end
  scenarios.
