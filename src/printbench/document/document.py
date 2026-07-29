from dataclasses import dataclass, field


@dataclass(slots=True)
class Document:
    width: float
    height: float

    _elements: list = field(default_factory=list)

    def add(self, element) -> None:
        self._elements.append(element)

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)
