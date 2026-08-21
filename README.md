# genetic-optimizer-ai

A standalone, zero-dependency Python package providing a **genetic algorithm optimizer** for evolving numeric parameter sets and a **rule-based task classifier** that maps natural-language descriptions to execution blueprints.

Both components rely only on the Python standard library (3.11+).

## Installation

```bash
pip install genetic-optimizer-ai
```

Or install from source:

```bash
git clone https://github.com/FlossWare/genetic-optimizer-ai.git
cd genetic-optimizer-ai
pip install .
```

## Quickstart

### Genetic Algorithm Optimization

Evolve parameters toward a fitness objective:

```python
from genetic_optimizer_ai import GeneticOptimizer, ParamBounds

# Define the parameter search space
params = [
    ParamBounds("x", -5.0, 5.0),
    ParamBounds("y", -5.0, 5.0),
]

# Create an optimizer with a fixed seed for reproducibility
optimizer = GeneticOptimizer(
    params=params,
    population_size=30,
    seed=42,
)

# Define a fitness function (maximize negative distance from origin)
def fitness(individual):
    x = individual.genes["x"]
    y = individual.genes["y"]
    return -(x**2 + y**2)

# Run 50 generations of evolution
best = optimizer.evolve(fitness, generations=50)

print(f"Best solution: x={best.genes['x']:.4f}, y={best.genes['y']:.4f}")
print(f"Fitness: {best.fitness:.4f}")
print(f"Population stats: {optimizer.population_stats()}")
print(f"Diversity: {optimizer.diversity():.4f}")
```

### Task Classification

Classify task descriptions into execution blueprints:

```python
from genetic_optimizer_ai import RuleBasedTaskClassifier

classifier = RuleBasedTaskClassifier()

# Classify different task types
tasks = [
    "Write a Python function to sort a list",
    "Research the latest trends in NLP",
    "Summarize this article for me",
    "What is the capital of France?",
    "Use multi-model consensus to evaluate this",
]

for task in tasks:
    blueprint = classifier.classify(task)
    print(f"Task: {task}")
    print(f"  Category: {blueprint.category}")
    print(f"  Models: {blueprint.models}")
    print(f"  Consensus: {blueprint.use_consensus}")
    print(f"  Timeout: {blueprint.timeout_seconds}s")
    print()
```

### Decorator-Based Optimization (ADR-0006)

Use the `@optimize` decorator for a concise, declarative approach:

```python
from genetic_optimizer_ai import optimize

@optimize(param_bounds={"x": (-5, 5), "y": (-5, 5)}, generations=50, seed=42)
def find_minimum(x: float, y: float) -> float:
    """Return fitness (higher is better). GA maximizes this."""
    return -(x**2 + y**2)

result = find_minimum()
print(f"Best params: {result.best_params}")
print(f"Fitness: {result.fitness:.6f}")
print(f"Return value: {result.value:.6f}")
```

## API Overview

### Genetic Optimizer

| Class / Function | Description |
|---|---|
| `Individual` | A candidate solution with `genes` (dict of floats) and `fitness` score |
| `ParamBounds` | Defines min/max range for an evolvable parameter |
| `GeneticOptimizer` | Population-based GA with tournament selection, uniform crossover, and Gaussian mutation |
| `GeneticOptimizer.evolve(fitness_fn, generations=1)` | Run N generations, return the best `Individual` |
| `GeneticOptimizer.population_stats()` | Min/max/mean/std of current population fitness |
| `GeneticOptimizer.diversity()` | Mean pairwise gene-space distance |

### Task Classifier

| Class / Function | Description |
|---|---|
| `ExecutionBlueprint` | Dataclass describing how a task should execute (category, models, consensus, timeout, retries) |
| `TaskClassifier` | Protocol defining the `.classify(task) -> ExecutionBlueprint` interface |
| `RuleBasedTaskClassifier` | Keyword-pattern implementation classifying into: `simple_qa`, `research`, `code_generation`, `consensus`, `summarization`, `translation` |

### Decorator

| Class / Function | Description |
|---|---|
| `@optimize(param_bounds, generations, ...)` | Decorator that runs a GA to find optimal parameters before executing the wrapped function |
| `OptimizeResult` | Dataclass with `best_params`, `fitness`, `value`, `generations_run`, `population_stats` |

## FlossWare Engineering Standards

This package complies with the [FlossWare Engineering Standards](https://github.com/FlossWare/engineering-standards). See [STANDARDS.md](STANDARDS.md) for full details.

| ADR | Requirement | How This Package Complies |
|---|---|---|
| ADR-0001 | Explicit Opt-In | Optimization only runs when the user explicitly calls `.evolve()` or invokes an `@optimize`-decorated function. No implicit background work. |
| ADR-0006 | Cross-Cutting Decorators | The `@optimize` decorator provides a composable, declarative interface for GA-based parameter tuning. |
| ADR-0008 | Free-First | Zero external dependencies -- stdlib only. |
| ADR-0009 | Core Principles | Modular components, composable via callables and protocols, contracts over implementations (`TaskClassifier` protocol). |
| ADR-0013 | Bandit-Based Model Selection | Complements Thompson Sampling (model-router-ai) for hyperparameter tuning of model selection strategies. |
| ADR-0017 | Agent-Neutral | No dependency on any agent runtime or orchestration engine. |

## License

MIT
