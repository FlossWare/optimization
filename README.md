# optimizer

**Reusable genetic and evolutionary optimization for FlossWare.**

This repository provides a standalone genetic algorithm implementation for evolving parameter sets. It is an optimization implementation, not an agent runtime, task router, or orchestration layer.

## Boundary

```text
OptimizationStrategy contract
          |
          v
      optimizer
          |
          v
candidate parameters -> fitness evaluation -> next generation
```

The optimizer can be used by Loom or other compatible systems without coupling it to Loom, a model provider, or a particular execution runtime.

## Task classification

The former package also exposed a rule-based task classifier that produced execution blueprints containing model, consensus, timeout, and retry decisions. That abstraction belongs to the superseded agent/task-routing architecture and is not part of the intended FlossWare architecture.

New work here should focus on reusable optimization algorithms and their contracts. Loom remains responsible for execution semantics; `strategy` owns reusable decision strategies such as Thompson Sampling and epsilon-greedy selection.

## Repository naming

The repository is named `optimizer`. Documentation, package metadata, examples, and links should use that name unless a specific published package name requires otherwise.
