"""Cross-cutting decorator for genetic optimization (ADR-0006).

Provides the ``@optimize`` decorator that wraps a fitness function with
a genetic algorithm, evolving parameters toward the optimal values before
executing the decorated function with those values.

This module uses only the Python standard library.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Any

from optimization.genetic_optimizer import (
    GeneticOptimizer,
    Individual,
    ParamBounds,
)


@dataclass
class OptimizeResult:
    """Result returned by an ``@optimize``-decorated function.

    Attributes:
        best_params: The best parameter values found by the GA.
        fitness: The fitness score of the best individual.
        value: The return value of the decorated function called with
            the best parameters.
        generations_run: Number of generations the GA executed.
        population_stats: Summary statistics of the final population.
    """

    best_params: dict[str, float]
    fitness: float
    value: Any
    generations_run: int
    population_stats: dict[str, float] = field(default_factory=dict)


def optimize(
    *,
    param_bounds: dict[str, tuple[float, float]],
    generations: int = 50,
    population_size: int = 20,
    mutation_rate: float = 0.1,
    crossover_rate: float = 0.7,
    seed: int | None = None,
) -> Callable:
    """Decorator that runs a GA to find optimal parameters for a function.

    The decorated function must accept keyword arguments matching the keys
    in *param_bounds* and return a float fitness score (higher is better).

    When the decorated function is called, the GA evolves parameters within
    the given bounds, then calls the original function one final time with
    the best parameters found. The return value is an :class:`OptimizeResult`.

    Parameters
    ----------
    param_bounds:
        Mapping of parameter names to ``(low, high)`` bounds.
        Example: ``{"temperature": (0.0, 2.0), "top_p": (0.0, 1.0)}``.
    generations:
        Number of GA generations to run.
    population_size:
        Number of individuals in the GA population.
    mutation_rate:
        Probability of mutating each gene per generation.
    crossover_rate:
        Probability of crossover between parents.
    seed:
        Optional random seed for reproducibility.

    Example
    -------
    ::

        @optimize(param_bounds={"x": (-5, 5), "y": (-5, 5)}, generations=50)
        def find_minimum(x: float, y: float) -> float:
            return -(x**2 + y**2)

        result = find_minimum()
        print(result.best_params)  # {'x': ~0.0, 'y': ~0.0}
        print(result.fitness)      # ~0.0

    Notes
    -----
    Optimization is explicit opt-in (ADR-0001): the GA only runs when
    the decorated function is called. No background optimization occurs.
    """

    bounds = [ParamBounds(name, low, high) for name, (low, high) in param_bounds.items()]

    def decorator(fn: Callable[..., float]) -> Callable[..., OptimizeResult]:

        @functools.wraps(fn)
        def wrapper(**override_kwargs: Any) -> OptimizeResult:
            # Allow callers to override GA settings per-call
            gen = override_kwargs.pop("_generations", generations)
            pop = override_kwargs.pop("_population_size", population_size)
            s = override_kwargs.pop("_seed", seed)

            ga = GeneticOptimizer(
                params=bounds,
                population_size=pop,
                mutation_rate=mutation_rate,
                crossover_rate=crossover_rate,
                seed=s,
            )

            def fitness_fn(ind: Individual) -> float:
                return fn(**ind.genes, **override_kwargs)

            best = ga.evolve(fitness_fn, generations=gen)

            # Call the function one final time with the best params
            final_value = fn(**best.genes, **override_kwargs)

            return OptimizeResult(
                best_params=dict(best.genes),
                fitness=best.fitness,
                value=final_value,
                generations_run=gen,
                population_stats=ga.population_stats(),
            )

        return wrapper

    return decorator
