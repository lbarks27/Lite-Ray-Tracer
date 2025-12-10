# Kalman Filter Visualization Scaffold

This document describes the repository layout that will support Kalman filter
visualizations built with Matplotlib or Manim. The goal is to separate concerns
between data generation, filtering, and rendering while keeping dependencies
light until specific implementations are added.

## Directory overview

- `src/kalman_viz/config/` — central configuration dataclasses shared across
  pipelines and scripts.
- `src/kalman_viz/filters/` — filter interfaces and factories for different
  Kalman variants.
- `src/kalman_viz/simulations/` — synthetic scenario and trajectory generators
  used to produce measurement streams.
- `src/kalman_viz/data/` — data ingestion helpers for recorded or generated
  measurements.
- `src/kalman_viz/visualization/` — adapters that translate filter outputs into
  visualizations for Matplotlib or Manim.
- `src/kalman_viz/scripts/` — orchestration scripts and future CLI entry points.
- `docs/` — design notes, architecture decisions, and diagrams.
- `tests/` — unit tests and integration tests.

## Next steps

- Implement concrete Kalman filters (e.g., constant-velocity, extended) inside
  `src/kalman_viz/filters/`.
- Fill in trajectory generators in `src/kalman_viz/simulations/` for common
  motion models.
- Add data loaders for CSV or parquet sources to `src/kalman_viz/data/`.
- Choose a rendering backend via `VisualizationConfig` and implement the
  corresponding renderer class.
- Wire up a CLI in `src/kalman_viz/scripts/visualize.py` to drive demos from the
  command line.
