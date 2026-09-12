# genetic-optimizer-ai

**Reusable genetic/evolutionary optimization for FlossWare.**

This repository provides a standalone genetic algorithm implementation for evolving parameter sets. It is a strategy implementation, not an agent runtime or task router.

## Boundary

```text
OptimizationStrategy contract
          │
          ▼
 GeneticOptimizer
          │
          ▼
 candidate parameters → fitness → next generation
```

The optimizer can be used by Loom or other compatible systems without becoming coupled to Loom, model providers, or a particular execution runtime.

## Task classification

The former package also exposed a rule-based task classifier that produced execution blueprints containing model, consensus, timeout, and retry decisions. That abstraction belongs to the superseded agent/task-routing architecture and is no longer part of the intended FlossWare architecture.

New work should use Loom Intent, Worker, Arbiter, and Strategy contracts rather than extending `ExecutionBlueprint` or adding another task classifier.

## Relationship to Loom

Loom owns execution and orchestration. `genetic-optimizer-ai` supplies one reusable optimization implementation. Evaluation supplies fitness/reward signals; Knowledge records validated learnings; model selection is one possible optimization workload.

## License

MIT
