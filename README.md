# PrintBench

PrintBench is an open-source Python library for generating precision print characterization targets.

The project is intended to support UV, inkjet, laser, and other digital printing systems by providing reproducible test patterns for evaluating:

- Registration accuracy
- Nozzle performance
- Line quality
- Resolution
- Dot gain
- Halftoning
- Geometric accuracy

PrintBench is designed as a reusable geometry and drawing library first, with printer-specific target generation built on top of it.

## Project Status

🚧 Early development

The current focus is building the core geometry library that will support all future drawing operations.

## Development

The project uses:

- Python 3.14
- Black
- Ruff
- Pytest

Typical workflow:

```bash
python -m black .
python -m ruff check .
python -m pytest
```