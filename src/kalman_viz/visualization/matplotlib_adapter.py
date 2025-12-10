"""Matplotlib-based rendering scaffolding."""

from __future__ import annotations

from pathlib import Path

from kalman_viz.config import VisualizationConfig
from kalman_viz.filters.base import BaseKalmanFilter
from kalman_viz.simulations.scenario import SimulationScenario


class MatplotlibRenderer:
    """Generate static or animated plots using Matplotlib."""

    def __init__(self, config: VisualizationConfig) -> None:
        self.config = config

    def render(self, scenario: SimulationScenario, filter_: BaseKalmanFilter) -> Path:
        """Render the scenario using Matplotlib primitives."""

        raise NotImplementedError(
            "Matplotlib renderer is a stub for early visualization experiments."
        )
