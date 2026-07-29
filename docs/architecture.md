# PrintBench Architecture

## Philosophy

PrintBench favors readability, explicitness, and composition over cleverness.

The code should describe the problem domain rather than the implementation details.

When multiple designs are possible, choose the one that most clearly expresses intent.

## Geometry

Geometry is independent of any output format.

The geometry library uses a Cartesian coordinate system.

Origin:
    (0,0)

Axes:
    +X → right
    +Y ↑ up

Geometry objects never know whether they will eventually be rendered as:

- SVG
- Eufy
- DXF
- PDF
- Bitmap

Those are rendering concerns.

## Documents

A Document represents a view of geometry.

A document owns:

- frame
- page size
- units
- drawable objects

A document does not know how to render itself.

## Renderers

Renderers translate geometry into an output format.

Examples:

- SVG
- Eufy
- DXF

A renderer is responsible for coordinate conversion.

**Geometry is never modified to satisfy an output format.**