"""optimization -- reusable genetic and evolutionary optimization.

A standalone, zero-dependency Python package providing:

- A genetic algorithm for evolving numeric parameter sets toward a
  caller-supplied fitness objective.

Both components rely only on the Python standard library.
"""

from __future__ import annotations

from optimization.decorators import OptimizeResult, optimize
from optimization.genetic_optimizer import (
    DEFAULT_PARAMS,
    GeneticOptimizer,
    Individual,
    ParamBounds,
)
__all__ = [
    "DEFAULT_PARAMS",
    "GeneticOptimizer",
    "Individual",
    "OptimizeResult",
    "ParamBounds",
    "optimize",
]

__version__ = "0.1"
