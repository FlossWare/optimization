# FlossWare Engineering Standards Compliance

This package adheres to the [FlossWare Engineering Standards](https://github.com/FlossWare/engineering-standards).

## Applicable ADRs

### ADR-0001: Explicit Opt-In

Optimization never runs automatically. Users must explicitly:
1. Create a `GeneticOptimizer` instance and call `.evolve()`
2. Or apply the `@optimize` decorator and call the decorated function

No background threads, no import-time side effects, no implicit optimization.

### ADR-0006: Cross-Cutting Decorators

The `@optimize` decorator provides a convenience layer for GA-based parameter tuning:

```python
from genetic_optimizer_ai import optimize

@optimize(param_bounds={"x": (-5, 5), "y": (-5, 5)}, generations=50)
def find_minimum(x: float, y: float) -> float:
    return -(x**2 + y**2)

result = find_minimum()  # returns OptimizeResult
```

The decorator composes cleanly with other decorators and does not modify the
original function's signature or behavior -- it wraps it.

### ADR-0008: Free-First

Zero external dependencies. The entire package uses only the Python standard
library (`math`, `random`, `re`, `dataclasses`, `typing`, `functools`).

### ADR-0009: Core Principles

- **Modular**: `GeneticOptimizer`, `RuleBasedTaskClassifier`, and `@optimize`
  are independent components that can be used separately.
- **Composable**: The optimizer accepts any `Callable[[Individual], float]` as
  a fitness function. The classifier is pluggable via the `TaskClassifier`
  protocol.
- **Contracts over implementations**: `TaskClassifier` is a `Protocol` -- any
  class implementing `.classify(task) -> ExecutionBlueprint` satisfies it
  without inheritance.

### ADR-0013: Bandit-Based Model Selection

The genetic optimizer complements Thompson Sampling (from
[model-router-ai](https://github.com/FlossWare/model-router-ai)) for
hyperparameter tuning of model selection strategies. Typical usage:

- **Thompson Sampling** selects which model to route a request to (exploration
  vs. exploitation tradeoff).
- **GeneticOptimizer** tunes the parameters governing that selection (e.g.,
  temperature, prior strength, weight decay) by evolving parameter sets that
  maximize routing quality metrics.

```python
from genetic_optimizer_ai import GeneticOptimizer, ParamBounds

# Evolve Thompson Sampling hyperparameters
params = [
    ParamBounds("prior_alpha", 0.1, 10.0),
    ParamBounds("prior_beta", 0.1, 10.0),
    ParamBounds("decay_rate", 0.01, 0.5),
]

optimizer = GeneticOptimizer(params=params, population_size=30, seed=42)
best = optimizer.evolve(evaluate_routing_quality, generations=100)
```

### ADR-0017: Agent-Neutral

This package has no dependency on any specific agent runtime, framework, or
orchestration engine. It works with:

- Standalone Python scripts
- Any LLM agent framework (LangChain, CrewAI, AutoGen, custom)
- Any orchestration system (Kubernetes, Celery, custom fleet)
- Any model provider (OpenAI, Anthropic, Google, local models)

The `TaskClassifier` protocol and `GeneticOptimizer` class are pure Python
with no runtime assumptions.
