# genetic-optimizer-ai Integration Guide

Install:
```bash
pip install "git+https://github.com/FlossWare/genetic-optimizer-ai.git"
```

---

## Claude Code

### CLAUDE.md snippet

```markdown
## Optimization (genetic-optimizer-ai)

This project uses `genetic-optimizer-ai` to evolve parameters via genetic algorithm
and classify tasks into execution blueprints.

```python
from genetic_optimizer_ai import optimize, GeneticOptimizer, RuleBasedTaskClassifier

@optimize(
    bounds={"temperature": (0.0, 2.0), "top_p": (0.0, 1.0)},
    generations=50, population=30,
)
def fitness(temperature: float, top_p: float) -> float:
    # Return higher = better
    return score_from_experiment(temperature, top_p)
```
```

### Skills

Create `.claude/skills/optimize-params.md`:
```markdown
---
name: optimize-params
description: Run a genetic algorithm to find optimal parameters
---

Use genetic-optimizer-ai's GeneticOptimizer to evolve parameters.
Define bounds, fitness function, then run for N generations.
Report the best individual and its fitness score.
```

---

## OpenAI Codex

### AGENTS.md snippet
```markdown
## Parameter Optimization

Use `genetic-optimizer-ai` for hyperparameter tuning:

```python
from genetic_optimizer_ai import optimize, GeneticOptimizer, ParamBounds

@optimize(bounds={"lr": (1e-5, 1e-2), "batch": (8, 128)}, generations=100)
def fitness(lr: float, batch: float) -> float:
    return evaluate_model(lr=lr, batch_size=int(batch))
```
```

---

## Cursor

### .cursorrules snippet
```
Use genetic-optimizer-ai for parameter optimization:
- @optimize(bounds={...}, generations=N) decorator for simple cases
- GeneticOptimizer class for full control (custom crossover, mutation rates)
- RuleBasedTaskClassifier to map task descriptions to execution plans

Import from: from genetic_optimizer_ai import optimize, GeneticOptimizer, RuleBasedTaskClassifier
Package: pip install "git+https://github.com/FlossWare/genetic-optimizer-ai.git"
Zero dependencies — stdlib only.
```

---

## Crush

### Configuration
```python
from crush import Agent
from genetic_optimizer_ai import optimize, RuleBasedTaskClassifier

classifier = RuleBasedTaskClassifier()

class OptimizingAgent(Agent):
    async def plan(self, task: str):
        blueprint = classifier.classify(task)
        return blueprint

    @optimize(bounds={"temperature": (0.0, 2.0)}, generations=20)
    def tune_temperature(self, temperature: float) -> float:
        return self.evaluate_output_quality(temperature)
```

---

## Generic Python Agent

### Usage patterns
```python
from genetic_optimizer_ai import (
    GeneticOptimizer, ParamBounds, Individual,
    RuleBasedTaskClassifier, ExecutionBlueprint,
    optimize, OptimizeResult,
)

# 1. Decorator approach — simplest
@optimize(
    bounds={"temperature": (0.0, 2.0), "top_p": (0.0, 1.0)},
    generations=50, population=30,
)
def fitness(temperature: float, top_p: float) -> float:
    return score(temperature, top_p)

result: OptimizeResult = fitness()

# 2. Programmatic approach — full control
bounds: ParamBounds = {"lr": (1e-5, 1e-2), "dropout": (0.0, 0.5)}
optimizer = GeneticOptimizer(bounds=bounds, population_size=50)

for gen in range(100):
    optimizer.step(fitness_fn=my_fitness)

best: Individual = optimizer.best
print(f"Best params: {best.genes}, fitness: {best.fitness}")

# 3. Task classification
classifier = RuleBasedTaskClassifier()
blueprint: ExecutionBlueprint = classifier.classify(
    "Analyze customer sentiment from support tickets"
)
print(f"Strategy: {blueprint.strategy}")
print(f"Models: {blueprint.recommended_models}")
```

---

## Cross-Package Integration

### With resilience-ai + observability-ai
```python
from resilience_ai import with_retry
from observability_ai import track_execution, ExecutionTelemetry
from genetic_optimizer_ai import optimize

telemetry = ExecutionTelemetry()

@optimize(bounds={"temperature": (0.0, 2.0)}, generations=30)
@with_retry(max_attempts=3)
@track_execution(telemetry=telemetry, provider="experiment")
def fitness(temperature: float) -> float:
    return run_experiment(temperature)
```

### With consensus-ai
```python
from consensus_ai import with_consensus
from genetic_optimizer_ai import optimize

@optimize(bounds={"temperature": (0.0, 2.0)}, generations=20)
async def consensus_fitness(temperature: float) -> float:
    @with_consensus(models=["gpt-4o", "claude-sonnet", "gemini-flash"])
    async def evaluate(prompt: str, **kwargs) -> str:
        ...
    result = await evaluate(f"Rate quality at temp={temperature}")
    return float(result.split("/")[0])  # parse "8/10"
```
