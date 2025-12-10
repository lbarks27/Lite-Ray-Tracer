"""Scenario descriptions and result bundles for synthetic data generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from kalman_viz.filters.base import Measurement


@dataclass
class SimulationScenario:
    """Container for simulation metadata and generated series."""

    name: str
    measurements: Iterable[Measurement]
    dt: float

    @property
    def duration(self) -> float:
        """Return an approximate duration of the scenario in seconds."""

        return len(list(self.measurements)) * self.dt
