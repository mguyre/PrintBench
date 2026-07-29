from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    """
    A two-dimensional point expressed in millimeters.

    The PrintBench geometry engine uses millimeters as its
    internal unit of measure.
    """

    x: float
    y: float
