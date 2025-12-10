"""Manim-based rendering scaffolding."""

from __future__ import annotations

from pathlib import Path

from kalman_viz.config import VisualizationConfig
from kalman_viz.filters.base import BaseKalmanFilter
from kalman_viz.simulations.scenario import SimulationScenario


class ManimRenderer:
    """Prepare a Manim scene from filter outputs.

    This class intentionally avoids importing Manim directly so that the base
    repository remains lightweight until animation work begins.
    """

    def __init__(self, config: VisualizationConfig) -> None:
        self.config = config

    def render(self, scenario: SimulationScenario, filter_: BaseKalmanFilter) -> Path:
        """Render a video and return the path to the generated asset."""

        raise NotImplementedError("Manim renderer is a future extension point.")
