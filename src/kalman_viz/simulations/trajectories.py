"""Trajectory generation stubs for seeding filters with synthetic data."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from kalman_viz.filters.base import Measurement


class TrajectoryGenerator(Protocol):
    """Protocol for classes that synthesize measurement streams."""

    def generate(self) -> Iterable[Measurement]:
        """Yield synthetic measurements for downstream filters."""


@dataclass
class CircularTrajectory:
    """Placeholder circular motion generator for early visual tests."""

    radius: float
    angular_rate: float

    def generate(self) -> Iterable[Measurement]:  # type: ignore[override]
        raise NotImplementedError("CircularTrajectory is a stub for future work.")
