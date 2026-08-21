"""Tests for the genetic_optimizer_ai package."""

from __future__ import annotations

import math

import pytest

from genetic_optimizer_ai import (
    ExecutionBlueprint,
    GeneticOptimizer,
    Individual,
    OptimizeResult,
    ParamBounds,
    RuleBasedTaskClassifier,
    TaskClassifier,
    optimize,
)


# ── GeneticOptimizer tests ──────────────────────────────────────────────


class TestIndividual:
    def test_defaults(self) -> None:
        ind = Individual()
        assert ind.genes == {}
        assert ind.fitness == 0.0

    def test_custom_values(self) -> None:
        ind = Individual(genes={"x": 1.5, "y": -0.3}, fitness=42.0)
        assert ind.genes["x"] == 1.5
        assert ind.fitness == 42.0


class TestParamBounds:
    def test_fields(self) -> None:
        pb = ParamBounds("temperature", 0.0, 2.0)
        assert pb.name == "temperature"
        assert pb.low == 0.0
        assert pb.high == 2.0


class TestGeneticOptimizer:
    def test_initialize_creates_population(self) -> None:
        opt = GeneticOptimizer(population_size=10, seed=1)
        opt.initialize()
        assert len(opt.population) == 10
        assert opt.generation == 0

    def test_population_size_validation(self) -> None:
        with pytest.raises(ValueError, match="population_size must be >= 2"):
            GeneticOptimizer(population_size=1)

    def test_elitism_validation(self) -> None:
        with pytest.raises(ValueError, match="elitism must be less than"):
            GeneticOptimizer(population_size=5, elitism=5)

    def test_evolve_improves_fitness(self) -> None:
        """Fitness should improve (or stay the same) over many generations."""
        params = [ParamBounds("x", -5.0, 5.0)]
        opt = GeneticOptimizer(params=params, population_size=20, seed=42)

        # Maximize negative absolute value of x (optimum at x=0)
        def fitness(ind: Individual) -> float:
            return -abs(ind.genes["x"])

        best = opt.evolve(fitness, generations=50)
        assert best.fitness > -5.0  # should be much closer to 0

    def test_evolve_returns_best(self) -> None:
        params = [ParamBounds("x", 0.0, 10.0)]
        opt = GeneticOptimizer(params=params, population_size=10, seed=7)

        def fitness(ind: Individual) -> float:
            return ind.genes["x"]

        best = opt.evolve(fitness, generations=20)
        assert best.fitness == max(ind.fitness for ind in opt.population)

    def test_best_raises_before_evolve(self) -> None:
        opt = GeneticOptimizer(population_size=5, seed=0)
        with pytest.raises(RuntimeError, match="No evolution has been run"):
            _ = opt.best

    def test_population_stats(self) -> None:
        opt = GeneticOptimizer(population_size=5, seed=3)

        def fitness(ind: Individual) -> float:
            return sum(ind.genes.values())

        opt.evolve(fitness, generations=1)
        stats = opt.population_stats()
        assert set(stats.keys()) == {"min", "max", "mean", "std"}
        assert stats["min"] <= stats["mean"] <= stats["max"]
        assert stats["std"] >= 0.0

    def test_population_stats_empty(self) -> None:
        opt = GeneticOptimizer(population_size=5, seed=0)
        stats = opt.population_stats()
        assert stats == {"min": 0.0, "max": 0.0, "mean": 0.0, "std": 0.0}

    def test_diversity(self) -> None:
        params = [ParamBounds("x", 0.0, 10.0)]
        opt = GeneticOptimizer(params=params, population_size=10, seed=5)
        opt.initialize()
        d = opt.diversity()
        assert d > 0.0  # random population should have nonzero diversity

    def test_diversity_empty_or_single(self) -> None:
        opt = GeneticOptimizer(population_size=5, seed=0)
        assert opt.diversity() == 0.0
        opt.population = [Individual(genes={"x": 1.0})]
        assert opt.diversity() == 0.0

    def test_genes_stay_within_bounds(self) -> None:
        params = [ParamBounds("x", -1.0, 1.0)]
        opt = GeneticOptimizer(
            params=params,
            population_size=10,
            mutation_rate=1.0,
            mutation_sigma=5.0,
            seed=99,
        )

        def fitness(ind: Individual) -> float:
            return ind.genes["x"]

        opt.evolve(fitness, generations=20)
        for ind in opt.population:
            assert -1.0 <= ind.genes["x"] <= 1.0

    def test_deterministic_with_seed(self) -> None:
        def run(seed: int) -> float:
            params = [ParamBounds("x", 0.0, 10.0)]
            opt = GeneticOptimizer(params=params, population_size=10, seed=seed)
            best = opt.evolve(lambda i: i.genes["x"], generations=10)
            return best.fitness

        assert run(42) == run(42)


# ── TaskClassifier tests ────────────────────────────────────────────────


class TestExecutionBlueprint:
    def test_defaults(self) -> None:
        bp = ExecutionBlueprint(category="test")
        assert bp.category == "test"
        assert bp.models == []
        assert bp.use_consensus is False
        assert bp.timeout_seconds == 30.0
        assert bp.max_retries == 1
        assert bp.metadata == {}


class TestRuleBasedTaskClassifier:
    def test_code_generation(self) -> None:
        c = RuleBasedTaskClassifier()
        bp = c.classify("Write a Python function to sort a list")
        assert bp.category == "code_generation"
        assert bp.timeout_seconds == 45.0

    def test_research(self) -> None:
        c = RuleBasedTaskClassifier()
        bp = c.classify("Research the latest NLP trends")
        assert bp.category == "research"
        assert bp.max_retries == 2

    def test_consensus(self) -> None:
        c = RuleBasedTaskClassifier()
        bp = c.classify("Use multi-model consensus for this")
        assert bp.category == "consensus"
        assert bp.use_consensus is True

    def test_summarization(self) -> None:
        c = RuleBasedTaskClassifier()
        bp = c.classify("Summarize this article")
        assert bp.category == "summarization"

    def test_translation(self) -> None:
        c = RuleBasedTaskClassifier()
        bp = c.classify("Translate this to French")
        assert bp.category == "translation"

    def test_simple_qa_fallback(self) -> None:
        c = RuleBasedTaskClassifier()
        bp = c.classify("What is the capital of France?")
        assert bp.category == "simple_qa"
        assert bp.timeout_seconds == 15.0

    def test_implements_protocol(self) -> None:
        c = RuleBasedTaskClassifier()
        assert isinstance(c, TaskClassifier)

    def test_custom_rules(self) -> None:
        import re

        custom_rules = [
            (re.compile(r"\bspecial\b", re.IGNORECASE), "custom_category"),
        ]
        c = RuleBasedTaskClassifier(rules=custom_rules)
        bp = c.classify("This is a special task")
        assert bp.category == "custom_category"

    def test_custom_defaults(self) -> None:
        custom_defaults = {
            "simple_qa": {
                "models": ["turbo"],
                "timeout_seconds": 5.0,
            },
        }
        c = RuleBasedTaskClassifier(defaults=custom_defaults)
        bp = c.classify("What time is it?")
        assert bp.category == "simple_qa"
        assert bp.models == ["turbo"]
        assert bp.timeout_seconds == 5.0


# ── @optimize decorator tests ──────────────────────────────────────────


class TestOptimizeDecorator:
    def test_basic_optimization(self) -> None:
        @optimize(param_bounds={"x": (-5, 5)}, generations=30, seed=42)
        def neg_abs(x: float) -> float:
            return -abs(x)

        result = neg_abs()
        assert isinstance(result, OptimizeResult)
        assert result.fitness > -5.0
        assert "x" in result.best_params
        assert result.generations_run == 30

    def test_returns_optimize_result(self) -> None:
        @optimize(param_bounds={"x": (0, 10)}, generations=5, seed=1)
        def identity(x: float) -> float:
            return x

        result = identity()
        assert isinstance(result, OptimizeResult)
        assert hasattr(result, "best_params")
        assert hasattr(result, "fitness")
        assert hasattr(result, "value")
        assert hasattr(result, "generations_run")
        assert hasattr(result, "population_stats")

    def test_value_matches_fitness(self) -> None:
        """The value field should be the result of calling fn with best params."""

        @optimize(param_bounds={"x": (0, 10)}, generations=10, seed=7)
        def double(x: float) -> float:
            return x * 2

        result = double()
        # value is fn(best_params), fitness is the GA's best score
        expected = result.best_params["x"] * 2
        assert abs(result.value - expected) < 1e-10

    def test_multivariate(self) -> None:
        @optimize(
            param_bounds={"x": (-3, 3), "y": (-3, 3)},
            generations=40,
            seed=99,
        )
        def sphere(x: float, y: float) -> float:
            return -(x**2 + y**2)

        result = sphere()
        assert result.fitness > -18.0  # better than worst case (-9 - 9)
        assert "x" in result.best_params
        assert "y" in result.best_params

    def test_population_stats_populated(self) -> None:
        @optimize(param_bounds={"x": (0, 1)}, generations=5, seed=0)
        def f(x: float) -> float:
            return x

        result = f()
        assert "min" in result.population_stats
        assert "max" in result.population_stats
        assert "mean" in result.population_stats
        assert "std" in result.population_stats

    def test_deterministic_with_seed(self) -> None:
        def make():
            @optimize(param_bounds={"x": (0, 10)}, generations=10, seed=42)
            def f(x: float) -> float:
                return x

            return f()

        r1 = make()
        r2 = make()
        assert r1.fitness == r2.fitness
        assert r1.best_params == r2.best_params

    def test_override_generations_at_call(self) -> None:
        @optimize(param_bounds={"x": (0, 10)}, generations=5, seed=1)
        def f(x: float) -> float:
            return x

        result = f(_generations=2)
        assert result.generations_run == 2

    def test_extra_kwargs_passed_through(self) -> None:
        """Non-optimized kwargs should be forwarded to the function."""

        @optimize(param_bounds={"x": (0, 10)}, generations=5, seed=1)
        def weighted(x: float, scale: float = 1.0) -> float:
            return x * scale

        result = weighted(scale=2.0)
        expected = result.best_params["x"] * 2.0
        assert abs(result.value - expected) < 1e-10

    def test_preserves_function_name(self) -> None:
        @optimize(param_bounds={"x": (0, 1)}, generations=1, seed=0)
        def my_func(x: float) -> float:
            return x

        assert my_func.__name__ == "my_func"

    def test_no_auto_run_on_import(self) -> None:
        """ADR-0001: Optimization must not run automatically on decoration."""
        call_count = 0

        @optimize(param_bounds={"x": (0, 1)}, generations=1, seed=0)
        def tracked(x: float) -> float:
            nonlocal call_count
            call_count += 1
            return x

        # At this point, the function is decorated but NOT called
        assert call_count == 0

        # Only runs when explicitly called
        tracked()
        assert call_count > 0
