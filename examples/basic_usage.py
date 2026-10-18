#!/usr/bin/env python3
"""Basic optimization usage example.

Demonstrates parameter optimization via genetic algorithm
and task classification.
"""
from optimization import (
    GeneticOptimizer,
    ParamBounds,
    RuleBasedTaskClassifier,
    optimize,
)


@optimize(
    bounds={"x": (-10.0, 10.0), "y": (-10.0, 10.0)},
    generations=50,
    population=30,
)
def sphere_fitness(x: float, y: float) -> float:
    return -(x**2 + y**2)


def main() -> None:
    print("1. Decorator-based optimization")
    result = sphere_fitness()
    print(f"   Best params: x={result.best.genes['x']:.4f}, y={result.best.genes['y']:.4f}")
    print(f"   Fitness: {result.best.fitness:.4f}")
    print(f"   (Optimal is x=0, y=0 with fitness=0)\n")

    print("2. Programmatic optimization")
    bounds: ParamBounds = {"temperature": (0.0, 2.0), "top_p": (0.0, 1.0)}
    optimizer = GeneticOptimizer(bounds=bounds, population_size=20)
    for gen in range(30):
        optimizer.step(
            fitness_fn=lambda ind: -(
                (ind.genes["temperature"] - 0.7) ** 2
                + (ind.genes["top_p"] - 0.9) ** 2
            )
        )
    best = optimizer.best
    print(f"   Best: temp={best.genes['temperature']:.3f}, top_p={best.genes['top_p']:.3f}")
    print(f"   Fitness: {best.fitness:.4f}\n")

    print("3. Task classification")
    classifier = RuleBasedTaskClassifier()
    tasks = [
        "Summarize this document",
        "Write unit tests for the auth module",
        "Translate this email to Spanish",
    ]
    for task in tasks:
        blueprint = classifier.classify(task)
        print(f"   '{task}'")
        print(f"     -> strategy={blueprint.strategy}")


if __name__ == "__main__":
    print("optimization basic usage example")
    print("=" * 45)
    main()
