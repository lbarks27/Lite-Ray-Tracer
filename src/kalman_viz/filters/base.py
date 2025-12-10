"""Abstract base classes for Kalman-style filters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class State(Protocol):
    """Protocol describing the shape of a filter state used for typing only."""

    def as_vector(self) -> list[float]:
        """Return a vector-like representation for plotting."""


@dataclass
class Measurement:
    """Simple measurement container used in scaffold code."""

    values: list[float]
    timestamp: float


class BaseKalmanFilter(ABC):
    """Minimal interface that concrete filters should implement."""

    @abstractmethod
    def predict(self, dt: float) -> State:
        """Advance the filter state forward by ``dt`` seconds."""

    @abstractmethod
    def update(self, measurement: Measurement) -> State:
        """Ingest a new measurement into the filter state."""

    @abstractmethod
    def current_state(self) -> State:
        """Return the most recent state without mutating it."""
