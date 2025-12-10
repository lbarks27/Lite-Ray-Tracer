"""Visualization adapters for different rendering backends."""

from kalman_viz.visualization.manim_adapter import ManimRenderer
from kalman_viz.visualization.matplotlib_adapter import MatplotlibRenderer

__all__ = ["ManimRenderer", "MatplotlibRenderer"]
