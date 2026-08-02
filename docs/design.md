# PrintBench Design Notes

## Goals

- Readability is more important than cleverness.
- Favor explicit code over implicit behavior.
- Build only what the project currently needs.
- Every public API should have unit tests.

## Testing

- TDD: Red → Green → Refactor.
- One behavior per test.
- Parameterize tests when many inputs verify the same behavior.
- Test names should describe the behavior being verified.

## Geometry

- Point represents a location.
- Vector represents a displacement.
- Point + Point is intentionally unsupported.
- Point - Point returns a Vector.
- Point + Vector returns a Point.
- Point - Vector returns a Point.

## Comments

Comments explain *why*, not *what*.