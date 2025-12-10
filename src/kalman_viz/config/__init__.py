"""Configuration objects and helpers for the Kalman filter visualizer."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

Renderer = Literal["matplotlib", "manim"]


@dataclass
class VisualizationConfig:
    """User-facing configuration values for a visualization run.

    The attributes are intentionally simple so that they can be loaded from
    JSON, TOML, or YAML files once those loaders are added.
    """

    renderer: Renderer = "matplotlib"
    output_dir: Path = field(default_factory=lambda: Path("artifacts"))
    frame_rate: int = 30
    resolution: tuple[int, int] = (1920, 1080)


@dataclass
class DataSourceConfig:
    """Path-level configuration for generated or recorded trajectories."""

    measurements_path: Path = field(default_factory=lambda: Path("data/measurements.csv"))
    ground_truth_path: Path = field(default_factory=lambda: Path("data/ground_truth.csv"))
