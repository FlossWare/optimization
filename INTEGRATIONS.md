# optimization Integration Guide

Install from the repository:

```bash
pip install "git+https://github.com/FlossWare/optimization.git"
```

## Python usage

The package exposes a genetic algorithm and an explicit `@optimize` decorator. The caller supplies a fitness function; optimization does not invoke models, classify tasks, or orchestrate workflows.

```python
from optimization import GeneticOptimizer, Individual, ParamBounds, optimize

bounds = [
    ParamBounds("temperature", 0.0, 2.0),
    ParamBounds("top_p", 0.0, 1.0),
]

optimizer = GeneticOptimizer(params=bounds, seed=7)

def fitness(candidate: Individual) -> float:
    # Replace with a deterministic, caller-owned objective.
    return -(candidate.genes["temperature"] - 0.5) ** 2

best = optimizer.evolve(fitness, generations=20)
print(best.genes)

@optimize(param_bounds={"temperature": (0.0, 2.0)}, seed=7)
def score(temperature: float) -> float:
    return -(temperature - 0.5) ** 2

result = score()
print(result.best_params, result.fitness)
```

## Boundary

- `optimization` owns reusable optimization algorithms.
- `strategy` owns decision-selection algorithms.
- `evaluation` assesses outcomes and evidence.
- Loom owns execution semantics and orchestration.

Optimization must not override policy, authorization, safety, feasibility, or budget constraints.
