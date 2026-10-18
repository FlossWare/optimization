#!/bin/bash
# Add optimization integration to your CLAUDE.md
set -e

CLAUDE_MD="${CLAUDE_MD:-./CLAUDE.md}"

if [ ! -f "$CLAUDE_MD" ]; then
    echo "Creating $CLAUDE_MD..."
    touch "$CLAUDE_MD"
fi

cat >> "$CLAUDE_MD" << 'BLOCK'

## Optimization (optimization)

This project uses [optimization](https://github.com/FlossWare/optimization) for parameter optimization.

**Evolve parameters with genetic algorithms:**

```python
from optimization import optimize, GeneticOptimizer

@optimize(bounds={"temperature": (0.0, 2.0), "top_p": (0.0, 1.0)}, generations=50)
def fitness(temperature: float, top_p: float) -> float:
    return evaluate(temperature, top_p)
```

Install: `pip install "git+https://github.com/FlossWare/optimization.git"`
BLOCK

echo "Added optimization section to $CLAUDE_MD"
