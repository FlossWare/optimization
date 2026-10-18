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

**Implementation mismatch to resolve:** the current `optimization` package still exports `RuleBasedTaskClassifier`, `TaskClassifier`, and `ExecutionBlueprint` from `task_classifier.py`. Those symbols can still be imported today, so they must not be described as already removed. They represent legacy task-routing behavior and do not belong in the intended `optimization` boundary. Keep them documented as legacy until a separately reviewed migration removes or relocates them.

New work should focus on reusable optimization algorithms, explicit contracts, reproducible behavior, and tests. Keep runtime-specific orchestration out of this repository.

## Naming

The repository is named `optimization`; documentation and repository links use that name. The distribution is `optimization` and the canonical Python import package is `optimization`.
