#!/usr/bin/env python3
"""Claude Code hook: classify tasks and suggest optimization.

Install as a pre-tool hook in .claude/settings.json:
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "command": "python3 .claude/hooks/optimizer_hook.py"
    }]
  }
}
"""
import json
import sys

from genetic_optimizer_ai import RuleBasedTaskClassifier

classifier = RuleBasedTaskClassifier()


def main() -> None:
    event = json.load(sys.stdin)
    tool_input = event.get("tool_input", {})

    description = ""
    if isinstance(tool_input, dict):
        description = tool_input.get("description", "") or tool_input.get("prompt", "")

    if description:
        blueprint = classifier.classify(description)
        sys.stderr.write(
            f"Task classification: strategy={blueprint.strategy}\n"
        )

    print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
