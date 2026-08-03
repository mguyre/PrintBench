from dataclasses import dataclass

from printbench import Document


@dataclass(slots=True)
class SvgRenderer:
    #    width: float
    #    height: float

    def render(self, document: Document) -> str:
        return f'<svg width="{document.width}" ' f'height="{document.height}"></svg>'
