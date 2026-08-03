# PrintBench Design Notes

## Design Principles

- Prefer composition over duplication.
- Write code at the highest level of abstraction that correctly expresses the intent.
- Behavior belongs to the object that owns the data.
- Refactor only after the code demonstrates the need.
- Introduce complexity only when it solves a real problem.## Goals

## Goals

- Readability is more important than cleverness.
- Favor explicit code over implicit behavior.
- Build only what the project currently needs.
- Every public API should have unit tests.

## Testing

- TDD: Red → Green → Refactor.
- One behavior per test.
- Tests are executable specifications.
- Parameterize tests when many inputs verify the same behavior.
- Test names should describe the behavior being verified.
- Choose test data that makes implementation mistakes obvious. Avoid symmetric or repetitive values when they can hide bugs.

## Success Criteria

- A new developer should be able to understand the designby reading the public APIs before reading the implementations.

## Geometry

- Point represents a location.
- Vector represents a displacement.
- Point + Point is intentionally unsupported.
- Point - Point returns a Vector.
- Point + Vector returns a Point.
- Point - Vector returns a Point.

## Comments

Comments explain *why*, not *what*.

