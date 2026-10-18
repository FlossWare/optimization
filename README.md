# optimization

**Reusable genetic and evolutionary optimization for FlossWare.**

This repository provides optimization algorithms, beginning with a genetic algorithm implementation for evolving parameter sets. It is a reusable capability, not an agent runtime, task router, or orchestration layer.

## Boundary

```text
OptimizationStrategy contract
          |
          v
    optimization
          |
          v
candidate parameters -> fitness evaluation -> next generation
```

The algorithms can be used by Loom or other compatible systems without coupling them to Loom, a model provider, or a particular execution runtime.

## Responsibility split

- `optimization` owns reusable genetic and evolutionary optimization algorithms.
- `strategy` owns reusable decision strategies such as Thompson Sampling and epsilon-greedy selection. Strategies may use optimization algorithms where appropriate, but the two responsibilities are not interchangeable.
- `evaluation` owns reusable assessment of results against intended outcomes.
- Loom owns execution semantics and orchestration, not optimization algorithms.

Optimization must operate within externally enforced security, authorization, safety, and budget constraints. An algorithm cannot make an otherwise forbidden operation permissible.

## Scope

The former package also exposed a rule-based task classifier that produced execution blueprints containing model, consensus, timeout, and retry decisions. That abstraction belongs to the superseded agent/task-routing architecture and is not part of the intended FlossWare architecture.

New work should focus on reusable optimization algorithms, explicit contracts, reproducible behavior, and tests. Keep runtime-specific orchestration out of this repository.

## Naming

The repository is named `optimization`. Documentation, package metadata, examples, and links should use that name unless a published package name must remain compatible for a documented reason.
