#!/usr/bin/env python3
"""Basic usage of the optimization package."""

from optimization import GeneticOptimizer, Individual, ParamBounds, optimize


@optimize(
    param_bounds={"x": (-10.0, 10.0), "y": (-10.0, 10.0)},
    generations=50,
    population_size=30,
    seed=7,
)
def sphere_fitness(x: float, y: float) -> float:
    """Higher scores are better; the maximum is at (0, 0)."""
    return -(x**2 + y**2)


def main() -> None:
    print("1. Decorator-based optimization")
    result = sphere_fitness()
    print(f"   Best params: {result.best_params}")
    print(f"   Fitness: {result.fitness:.4f}")

    print("\n2. Programmatic optimization")
    bounds = [
        ParamBounds("temperature", 0.0, 2.0),
        ParamBounds("top_p", 0.0, 1.0),
    ]
    optimizer = GeneticOptimizer(params=bounds, population_size=20, seed=7)

    def fitness(candidate: Individual) -> float:
        return -(
            (candidate.genes["temperature"] - 0.7) ** 2
            + (candidate.genes["top_p"] - 0.9) ** 2
        )

    best = optimizer.evolve(fitness, generations=30)
    print(f"   Best: {best.genes}")
    print(f"   Fitness: {best.fitness:.4f}")


if __name__ == "__main__":
    main()
