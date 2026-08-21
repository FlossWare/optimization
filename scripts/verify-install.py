#!/usr/bin/env python3
"""Verify genetic-optimizer-ai installation."""
import sys


def main() -> int:
    try:
        from genetic_optimizer_ai import (
            GeneticOptimizer,
            Individual,
            OptimizeResult,
            ParamBounds,
            RuleBasedTaskClassifier,
            optimize,
        )
    except ImportError as e:
        print(f"FAIL: Cannot import genetic-optimizer-ai: {e}")
        print("Install: pip install 'git+https://github.com/FlossWare/genetic-optimizer-ai.git'")
        return 1

    from genetic_optimizer_ai import __version__

    print(f"genetic-optimizer-ai v{__version__} installed successfully.")
    print(f"  GeneticOptimizer:      {GeneticOptimizer}")
    print(f"  RuleBasedTaskClassifier: {RuleBasedTaskClassifier}")
    print(f"  Decorators:            @optimize")

    bounds: ParamBounds = {"x": (0.0, 10.0)}
    optimizer = GeneticOptimizer(bounds=bounds, population_size=10)
    optimizer.step(fitness_fn=lambda ind: -abs(ind.genes["x"] - 5.0))
    print("  Smoke test:            PASS")

    return 0


if __name__ == "__main__":
    sys.exit(main())
