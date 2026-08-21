#!/bin/bash
# Add genetic-optimizer-ai integration to your CLAUDE.md
set -e

CLAUDE_MD="${CLAUDE_MD:-./CLAUDE.md}"

if [ ! -f "$CLAUDE_MD" ]; then
    echo "Creating $CLAUDE_MD..."
    touch "$CLAUDE_MD"
fi

cat >> "$CLAUDE_MD" << 'BLOCK'

## Optimization (genetic-optimizer-ai)

This project uses [genetic-optimizer-ai](https://github.com/FlossWare/genetic-optimizer-ai) for parameter optimization.

**Evolve parameters with genetic algorithms:**

```python
from genetic_optimizer_ai import optimize, GeneticOptimizer

@optimize(bounds={"temperature": (0.0, 2.0), "top_p": (0.0, 1.0)}, generations=50)
def fitness(temperature: float, top_p: float) -> float:
    return evaluate(temperature, top_p)
```

Install: `pip install "git+https://github.com/FlossWare/genetic-optimizer-ai.git"`
BLOCK

echo "Added genetic-optimizer-ai section to $CLAUDE_MD"
