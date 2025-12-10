"""Data access helpers for measurements and ground truth used in demos."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from kalman_viz.filters.base import Measurement


def load_measurements(path: Path) -> Iterable[Measurement]:
    """Read a measurement file and yield typed measurements.

    The implementation is intentionally left blank so that different data
    backends (CSV, parquet, or synthetic generators) can be plugged in later.
    """

    raise NotImplementedError("Measurement loader is a scaffold for later work.")
