#!/usr/bin/env python3
"""Verify optimization installation."""
import sys


def main() -> int:
    try:
        from optimization import (
            GeneticOptimizer,
            Individual,
            OptimizeResult,
            ParamBounds,
            RuleBasedTaskClassifier,
            optimize,
        )
    except ImportError as e:
        print(f"FAIL: Cannot import optimization: {e}")
        print("Install: pip install 'git+https://github.com/FlossWare/optimization.git'")
        return 1

    from optimization import __version__

    print(f"optimization v{__version__} installed successfully.")
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
