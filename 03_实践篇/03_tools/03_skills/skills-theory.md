# Agent Skills: Concepts, Design and Execution

English | [Simplified Chinese](skills-theory.zh-CN.md)

## From conversation to repeatable work

A chatbot can explain a task. An agent can use available operations to perform it.
Recurring work needs more than an operation list: it also needs a procedure, input
requirements, verification and output conventions. A Skill packages that knowledge
as a directory containing `SKILL.md` and optional scripts and references.

For document processing, a model without a Skill may improvise extraction, miss
tables or omit verification. A document Skill can specify how to inspect the file,
choose an extractor, preserve structure and check the result. Reliability still
depends on tool availability and the quality of the instructions; installing a Skill
does not guarantee success or grant new permissions.

Skills can improve consistency, reuse task knowledge and keep infrequently needed
instructions out of the main prompt. Host support varies. The Agent Skills format
describes a portable core; product-specific discovery, permissions and metadata
require the relevant host's documentation.

## How a Skill is loaded

Progressive disclosure separates three stages:

1. Discovery: the host sees a Skill name and description.
2. Activation: when relevant, the host reads the instructions in `SKILL.md`.
3. Execution: the agent reads selected references and invokes scripts or tools.

The exact selection mechanism is host-dependent. Some hosts allow explicit Skill
invocation in addition to automatic matching. A description should state the task,
the kinds of requests that trigger it, and meaningful exclusions. Instructions
cannot assume all supporting files are loaded at discovery time.

For example, a weather Skill should trigger on a current-weather or forecast request
when a local script workflow is suitable. If the user explicitly asks to use an MCP
server, that instruction should take precedence over silently substituting the CLI.

## Descriptions and evaluation

Describe user intent rather than implementation trivia. Include the operations
actually supported: current weather, forecasts, city names and coordinates. Exclude
closely related requests the Skill cannot fulfill, such as historical climate analysis
if the bundled script only supports current and forecast endpoints.

Avoid extremely broad triggers such as "use for every question". If two Skills
overlap, narrow their descriptions and document the decision rule. Resolve conflicts
using the user's request and the host's instruction hierarchy, not by claiming a
Skill can override higher-priority instructions.

Evaluate both positive and negative examples. Include paraphrases, ambiguous inputs,
English and Chinese requests, missing credentials and upstream failures. Record which
cases activate the Skill, whether the selected operation is correct, and whether the
reported result is grounded in actual output. Change the description based on those
observations, then rerun the same evaluation set to detect regressions.

## Minimal structure

```text
w-example/
  SKILL.md
  scripts/        # Optional executable helpers
  references/     # Optional detailed documentation
  assets/         # Optional templates or other output resources
```

`SKILL.md` contains YAML frontmatter followed by Markdown instructions:

```markdown
---
name: w-example
description: Explain the concrete task and when this Skill should be selected.
---

# Example workflow

1. Check the required input and environment.
2. Run the documented operation.
3. Verify the result and report its limits.
```

The standard core is not a requirement to create every possible subdirectory.
Files such as `metadata.json`, `README.md`, `examples/` and `tests/` are optional
repository conventions unless a host explicitly requires them. Use readable paths
relative to the Skill root, and link references directly from the instructions.

Frontmatter fields such as `license`, `compatibility` and `metadata` can document
distribution or runtime needs. Fields such as `allowed-tools` may depend on host
support and do not grant operating-system permissions. Validate names and frontmatter
against the target host rather than inventing mandatory fields.

## A first Skill

Start with a narrow procedure that has a visible result. A greeting Skill might
specify how to greet a user in their preferred language and offer no scripts at all.
Add a script only when executable logic is useful. Do not build a framework around
a task that a few instructions already handle.

For a PDF workflow, explain when to extract text, when scanned pages require OCR,
how to preserve tables and how to verify page coverage. Extraction, form filling
and merging are distinct operations; document supported formats and dependencies.
Use an existing appropriate library rather than implementing a PDF parser.

Marketplaces and shared repositories can distribute Skills, but inspect their
instructions and scripts before installation. Installation location and activation
behavior are host-specific. A project-local Skill and a user-wide Skill can have
different visibility and precedence.

## Scripts that agents can execute reliably

Scripts should have explicit arguments, a useful `--help`, deterministic output where
possible and meaningful exit codes. Avoid interactive prompts in automated runs.
Validate required values before network or filesystem operations, and return a clear
error if credentials or dependencies are missing.

Prefer self-contained operations with few dependencies. Use Python's standard library
for argument parsing, paths, JSON and CSV. If a third-party dependency is necessary,
document it and use an existing environment or an explicit installation step. Do not
silently install packages or change the user's global environment during a query.

One-off runners such as `uvx`, `pipx` or `npx`, and compiled utilities invoked with Go,
can be appropriate when already available. They may require downloads and are not
interchangeable. Python inline dependency metadata (PEP 723), Deno, Bun and Ruby
each have their own runtime and dependency conventions. Choose one supported workflow
and document it rather than presenting all of them as prerequisites.

### A small CSV analysis example

This script reads a named numeric column, rejects malformed input, and emits JSON.
It needs only Python's standard library.

```python
import argparse
import csv
import json
import statistics
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Summarize a numeric CSV column.")
parser.add_argument("path", type=Path)
parser.add_argument("--column", required=True)
args = parser.parse_args()

try:
    with args.path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if args.column not in (reader.fieldnames or []):
            raise ValueError(f"Missing column: {args.column}")
        values = [float(row[args.column]) for row in reader]
    if not values:
        raise ValueError("The selected column contains no data rows.")
    print(json.dumps({"count": len(values), "mean": statistics.mean(values)}))
except (OSError, ValueError, csv.Error) as exc:
    print(json.dumps({"error": str(exc)}), file=sys.stderr)
    sys.exit(1)
```

The Skill instructions can explain how to choose a column, invoke the script and
interpret the mean. They should also explain that this simple example rejects blank
or nonnumeric values rather than silently omitting them. Add richer statistics only
when a concrete task requires them.

## Input and output contracts

Use CLI arguments for small inputs, structured JSON for larger machine-generated
requests, and files for substantial content. Document required fields, defaults,
accepted units and output destinations. Resolve relative paths against a documented
working directory, or pass absolute paths when the host's working directory is uncertain.
Check file existence, file type and write destination before processing.

Separate progress messages from machine-readable output. A CLI can put JSON on stdout
and diagnostics on stderr. Keep keys stable across languages. Translate human-readable
messages when requested while preserving names and user content exactly.

An expected output example is useful, but label fixture data as illustrative. A script's
success exit code alone does not establish semantic correctness: check that expected
fields, files or records were produced and that results correspond to the input.

## Failure handling

Distinguish invalid input, execution failures and unusable results. Invalid input can
often be corrected before a call. Execution failures include missing credentials,
network timeouts and filesystem errors. Result failures include empty data or missing
required fields even when the upstream HTTP request succeeded.

Catch errors at the appropriate boundary, emit useful messages and use nonzero exit
codes. Avoid exposing secrets, full authenticated URLs or sensitive data in tracebacks.
Do not treat all exceptions as a successful empty result. Retry only when the operation
and failure type make retry appropriate; repeated writes can have side effects.

Dependencies should be declared in setup instructions. Earlier patterns that install
missing packages automatically need careful environment and permission handling;
explicit setup is simpler and more reproducible for these examples. A virtual
environment is usually sufficient. Docker is optional when isolation or deployment
requirements justify the additional setup.

## Weather case: Skill versus MCP

The [weather case](cases/01_weather_skill/README.md) includes
`w-openweather/SKILL.md`, `scripts/weather.py` and offline tests. The CLI queries
OpenWeather directly and does not import an MCP server. It supports current weather,
5-day/3-hour forecasts, city or coordinate input, English by default and Chinese via
`--language zh`. Tomorrow is interpreted in the location's provider UTC offset.

The [weather MCP server](../02_mcp/mcp/01_weather-mcp-server/README.md) exposes
equivalent operations through discoverable tools. It needs a running service and
client connection. The Skill needs a host capable of reading instructions and running
the bundled script. Both need the same upstream API credentials for real queries.

Use the case README's exact setup and commands. Do not substitute mock data for live
weather or imply that a 3-hour forecast product provides an official daily minimum
and maximum. Its sampled range and precipitation probability need explicit labels.

## Creating and improving a Skill

Gather representative requests and define the expected result. Inspect available
tools, then decide which steps belong in prose, scripts, references or templates.
Write the smallest useful version, run realistic examples, verify artifacts and
revise based on observed failures. If a creation helper is available, use its validation
workflow without treating it as a replacement for task-level testing.

Keep a Skill portable by avoiding undocumented absolute repository paths. Bundle
the files it actually needs, explain credentials and runtime dependencies, and test
the installed copy separately when it differs from the project source. Update both
language editions when the workflow changes.

References: [Agent Skills specification](https://agentskills.io/home) and
[OpenAI Skills documentation](https://developers.openai.com/plugins/concepts/skills).
