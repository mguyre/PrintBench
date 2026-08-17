"""
Document model for PrintBench.

Responsibilities
----------------
A Document represents a collection of geometry within a frame.

A Document owns:
- page dimensions
- frame (viewport)
- drawable objects

A Document does NOT:
- render SVG
- generate XML
- perform coordinate conversions

Those responsibilities belong to renderers.
"""

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import ClassVar

from printbench.geometry import ClosedShape
from printbench.style import Style


@dataclass(slots=True)
class Document:
    """A collection of geometry within a Cartesian frame.

    All dimensions and coordinates are expressed in millimeters.
    """

    units: ClassVar[str] = "mm"
    width: float
    height: float
    default_style: Style = field(default_factory=Style)

    _elements: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("Document width must be positive.")

        if self.height <= 0:
            raise ValueError("Document height must be positive.")

    def add(self, element) -> None:
        self._elements.append(element)

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator:
        return iter(self._elements)


@dataclass(slots=True)
class ClipContainer:
    """Contains entities clipped to a closed shape."""

    shape: ClosedShape
    _elements: list = field(default_factory=list)

    def __init__(self, shape: ClosedShape) -> None:
        if not isinstance(shape, ClosedShape):
            raise TypeError("shape must be a ClosedShape")

        self.shape = shape
        self._elements = []

    def add(self, entity) -> None:
        self._elements.append(entity)

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)


@dataclass(slots=True)
class Group:
    """Contains related entities."""

    _elements: list = field(default_factory=list)

    def __init__(self) -> None:
        self._elements = []

    def add(self, entity) -> None:
        self._elements.append(entity)

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)
