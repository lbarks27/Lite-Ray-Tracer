"""High-level orchestration script for future visualization demos."""

from __future__ import annotations

from kalman_viz.config import VisualizationConfig
from kalman_viz.filters import BaseKalmanFilter, build_filter
from kalman_viz.simulations import SimulationScenario
from kalman_viz.visualization import ManimRenderer, MatplotlibRenderer


def visualize(scenario: SimulationScenario, config: VisualizationConfig) -> None:
    """Run the configured visualization pipeline for a scenario."""

    filter_: BaseKalmanFilter = build_filter(config)
    renderer = _select_renderer(config)
    renderer.render(scenario, filter_)


def _select_renderer(config: VisualizationConfig):
    if config.renderer == "matplotlib":
        return MatplotlibRenderer(config)
    if config.renderer == "manim":
        return ManimRenderer(config)
    raise ValueError(f"Unsupported renderer: {config.renderer}")
