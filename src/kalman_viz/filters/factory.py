"""Factory helpers for building filter instances from configuration."""

from __future__ import annotations

from typing import Any

from kalman_viz.config import VisualizationConfig
from kalman_viz.filters.base import BaseKalmanFilter


def build_filter(config: VisualizationConfig, **kwargs: Any) -> BaseKalmanFilter:
    """Return a filter implementation based on a configuration value.

    This is a placeholder that will eventually select between variants such as
    a constant-velocity or constant-acceleration Kalman filter, and extended or
    unscented versions as the project grows.
    """

    raise NotImplementedError(
        "Filter factory is a scaffold only; choose an implementation when ready."
    )
