"""optimization -- Genetic algorithm optimizer and task classifier.

A standalone, zero-dependency Python package providing:

- A genetic algorithm for evolving numeric parameter sets toward a
  caller-supplied fitness objective.
- A rule-based task classifier that maps natural-language descriptions
  to execution blueprints.

Both components rely only on the Python standard library.
"""

from __future__ import annotations

from optimization.genetic_optimizer import (
    DEFAULT_PARAMS,
    GeneticOptimizer,
    Individual,
    ParamBounds,
)
from optimization.decorators import (
    OptimizeResult,
    optimize,
)
from optimization.task_classifier import (
    ExecutionBlueprint,
    RuleBasedTaskClassifier,
    TaskClassifier,
)

__all__ = [
    "DEFAULT_PARAMS",
    "ExecutionBlueprint",
    "GeneticOptimizer",
    "Individual",
    "OptimizeResult",
    "ParamBounds",
    "RuleBasedTaskClassifier",
    "TaskClassifier",
    "optimize",
]

__version__ = "0.1"
