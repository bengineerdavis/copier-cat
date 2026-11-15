"""Copy-safe help examples for the proposed copier-cat assembly CLI.

Human examples use harmless placeholders and state their effects. Agent examples
use explicit operands and machine-readable output; formatting is never consent.
This file is a prototype contract, not a production command implementation.
"""

from __future__ import annotations

import json

TOP_LEVEL_HELP = """copier-cat: compose and adopt ordinary Copier templates.

Human workflow:
  copier-cat --help
  copier-cat assemble --help
  copier-cat stack list

Agent workflow:
  copier-cat help --json
  copier-cat assemble --help --json
  copier-cat assemble example-project --stack example-stack --json

`ccc` is the local alias; `copier-cat` is the unambiguous installed command.
Read-only previews do not need --yes. Only an explicit write approval creates
files. See each command's help for its destination and approval scope.
"""

ASSEMBLE_HELP = """Assemble a new project from a named stack.

Usage: copier-cat assemble [OPTIONS] DESTINATION

Arguments:
  DESTINATION  Directory for the new project, for example ./example-project.
               This is not a template or stack name.

Options:
  --stack STACK  Named reusable template composition, for example example-stack.
                 Required for JSON and other noninteractive assembly.
  --dry-run      Resolve and display the plan without creating project files.
  --guided       Review human-readable answer and composition questions.
  --json         Emit a read-only machine-readable plan; never implies consent.
  --yes          Approve only the displayed new-destination write scope.
  --help         Show this human-readable help.
  --help --json  Emit the machine-readable command/argument/effect contract.

Examples:
  # Read-only: inspect how example-stack would create ./example-project.
  copier-cat assemble example-project --stack example-stack --dry-run

  # Interactive: review the plan and explicitly approve writes to the destination.
  copier-cat assemble example-project --stack example-stack

  # Agent: read-only JSON plan; no project writes and no approval flag required.
  copier-cat assemble example-project --stack example-stack --json

  # Agent: explicit approval to write only the displayed new destination.
  copier-cat assemble example-project --stack example-stack --json --yes

Copier equivalent: copier renders each template; cc composes the results and
leaves native answers files for `copier update -a ANSWERS_FILE`.

Exit codes: 0 success or read-only preview; 1 review required; 2 usage/error.
"""

ASSEMBLE_SCHEMA = {
    "schema_version": 1,
    "command": "copier-cat assemble",
    "operation": "assemble",
    "description": "Assemble a new project from a named stack.",
    "usage": "copier-cat assemble [OPTIONS] DESTINATION",
    "read_only": False,
    "writes": True,
    "approval_scope": "displayed-new-destination-only",
    "arguments": [
        {
            "name": "destination",
            "required": True,
            "value_name": "DESTINATION",
            "description": "New project directory; not a stack or template name.",
            "example": "./example-project",
        }
    ],
    "options": [
        {
            "flags": ["--stack"],
            "value_name": "STACK",
            "required_noninteractive": True,
            "description": "Named reusable template composition.",
            "example": "example-stack",
        },
        {
            "flags": ["--dry-run"],
            "description": "Resolve and display the plan without creating project files.",
            "effect": "read-only",
            "read_only": True,
            "writes": False,
        },
        {
            "flags": ["--guided"],
            "description": "Review human-readable answer and composition questions.",
            "effect": "interactive-review",
            "read_only": False,
            "writes": True,
        },
        {
            "flags": ["--json"],
            "description": "Emit a read-only machine-readable plan; never implies consent.",
            "effect": "read-only",
            "read_only": True,
            "writes": False,
            "implies_consent": False,
        },
        {
            "flags": ["--yes"],
            "description": "Approve only the displayed new-destination write scope.",
            "effect": "approve-write",
            "read_only": False,
            "writes": True,
            "scope": "displayed-new-destination-only",
        },
        {
            "flags": ["--help"],
            "description": "Show human-readable command help.",
            "effect": "read-only",
            "read_only": True,
            "writes": False,
        },
        {
            "flags": ["--help", "--json"],
            "description": "Emit this command's machine-readable discovery contract.",
            "effect": "read-only",
            "read_only": True,
            "writes": False,
        },
    ],
    "examples": [
        {
            "command": "copier-cat assemble example-project --stack example-stack",
            "description": "Review the plan and approve writing the new destination interactively.",
            "audience": ["human"],
            "read_only": False,
            "writes": True,
            "approval_scope": "interactive-displayed-new-destination-only",
        },
        {
            "command": "copier-cat assemble example-project --stack example-stack --dry-run",
            "description": "Inspect the assembly plan without creating files.",
            "audience": ["human", "agent"],
            "read_only": True,
            "writes": False,
            "destination": "./example-project",
            "stack": "example-stack",
        },
        {
            "command": "copier-cat assemble example-project --stack example-stack --json",
            "description": "Inspect the assembly plan without creating files.",
            "audience": ["human", "agent"],
            "read_only": True,
            "writes": False,
            "destination": "./example-project",
            "stack": "example-stack",
        },
        {
            "command": "copier-cat assemble example-project --stack example-stack --json --yes",
            "description": "Approve creation of only the displayed new project directory.",
            "audience": ["human", "agent"],
            "read_only": False,
            "writes": True,
            "approval_scope": "displayed-new-destination-only",
        },
    ],
    "exit_codes": {"0": "success or read-only preview", "1": "review required", "2": "usage/error"},
    "copier_equivalent": "copier update -a ANSWERS_FILE for each rendered template",
}


SCHEMA = ASSEMBLE_SCHEMA  # Backwards-compatible name for the focused example.

HELP_SCHEMA = {
    "schema_version": 1,
    "command": "copier-cat help",
    "operation": "discover",
    "description": "Discover copier-cat commands without executing them.",
    "usage": "copier-cat help --json",
    "read_only": True,
    "writes": False,
    "commands": [ASSEMBLE_SCHEMA],
    "examples": [
        {
            "command": "copier-cat help --json",
            "description": "List command descriptions and examples as JSON.",
            "audience": ["human", "agent"],
            "read_only": True,
            "writes": False,
        },
        {
            "command": "copier-cat assemble --help --json",
            "description": "Inspect only the assemble command contract.",
            "audience": ["human", "agent"],
            "read_only": True,
            "writes": False,
        },
    ],
}


def main() -> None:
    print(json.dumps(HELP_SCHEMA, separators=(",", ":")))


if __name__ == "__main__":
    main()
