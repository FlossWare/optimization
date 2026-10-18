"""Tests for the optimization package."""

from __future__ import annotations

import math

import pytest

from optimization import (
    GeneticOptimizer,
    Individual,
    OptimizeResult,
    ParamBounds,
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
