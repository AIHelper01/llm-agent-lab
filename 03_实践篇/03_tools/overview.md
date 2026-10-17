# Agents and Tools

English | [Simplified Chinese](overview.zh-CN.md)

## From agents to tool use

An agent perceives an environment, chooses actions, and uses their results to
pursue a goal. Sensors can be cameras, microphones, application events or API
responses. Actuators can be physical devices, code execution or service calls.
Autonomy describes how much decision making the system performs within its
constraints. It does not remove the need for validation or human oversight.

Traditional agent designs include simple reflex rules, models of internal state,
goal-based planning, utility-based decisions and learning. A thermostat illustrates
a reflex rule: when temperature crosses a threshold, switch the heater. Stateful
systems can account for observations that are incomplete or arrive over time.

An LLM adds a flexible natural-language interface and a way to propose plans and
tool arguments. It does not automatically provide current facts, reliable state or
permission to act. The surrounding application supplies these capabilities.
A travel assistant might clarify dates, query weather, propose an itinerary, and
revise it when the user changes the budget. Booking remains a separate action
with explicit application controls.

## Function Calling

Function Calling lets a model request a named function with structured arguments.
The application describes available functions using schemas. The model selects a
function and produces arguments; application code validates and executes them,
then returns the result to the model for a user-facing answer.

The usual loop is:

1. Send the user request and tool definitions to the model.
2. Receive an assistant response containing zero, one or several tool calls.
3. Validate names and arguments and execute the permitted functions.
4. Return each result with its matching tool-call identifier.
5. Ask the model to continue, repeating if the application supports further calls.

Training and provider support determine whether a model can produce usable tool
calls. Check the exact deployed model and API rather than assuming every model
in a family has the same support. A model proposes a call; the runtime executes it.

The [Function Calling notebook](01_function-calling/01_fc-practice.ipynb) stays
deliberately small: a direct weather function, a JSON schema, a no-tool comparison,
a single-tool exchange and a two-tool selection example. It uses Chat Completions
through an OpenAI-compatible client. Responses API examples use a different message
format, so do not mix the two formats. See the
[official Function Calling guide](https://developers.openai.com/api/docs/guides/function-calling).

## Why MCP exists

Writing a separate adapter for each host/tool combination creates duplication.
Model Context Protocol standardizes capability discovery and exchange between a
host's MCP client and an MCP server. A server can expose tools, resources and
prompts to compatible hosts. This improves reuse while leaving tool selection,
user interaction and authorization under the host's control.

MCP is an integration protocol. Function Calling is a model/API mechanism for
requesting execution. A host can translate discovered MCP tools into model tool
definitions and route requests to the appropriate MCP client. A server need not
contain a model, and installing a server does not make a model an agent by itself.

### Architecture and lifecycle

The host manages the overall application and model conversation. Each client
maintains a protocol connection to a server. Servers expose focused capabilities,
possibly backed by local files, databases or external HTTP APIs.

The protocol data layer uses JSON-RPC requests, responses and notifications. The
transport layer carries those messages, commonly through stdio or Streamable HTTP.
The SDK 1.x examples in this repository initialize a session, negotiate capabilities,
exchange the initialized notification, discover tools, and make calls. These examples
describe that SDK's protocol generation; consult the negotiated protocol version
before applying newer documentation to old clients.

```text
Host -> Client -> Server: initialize
Server -> Client: supported protocol and capabilities
Client -> Server: initialized notification
Client -> Server: tools/list
Client -> Server: tools/call(name, arguments)
Server -> Client: structured and/or text content
```

Notifications communicate events without a request response. A server advertising
tool-list-change support can notify clients when the available list changes; the
host decides when to refresh and how to expose the new capabilities.

### Protocol primitives

| Primitive | Typical purpose | Example |
| --- | --- | --- |
| Tools | Execute operations | Query weather or rename a file |
| Resources | Read contextual data | Read a document through a resource URI |
| Prompts | Reuse message templates | Start a structured review |
| Roots | Describe client-provided workspace scope | Identify a project directory |
| Sampling | Request model assistance through the client | Analyze a server-side result |
| Elicitation | Request additional user input where supported | Clarify travel preferences |

Roots describe scope; they are not an operating-system sandbox. Sampling and
elicitation depend on negotiated capabilities and host policy. Tool results and
resource content remain untrusted inputs to the model.

The [MCP theory](02_mcp/01_mcp-theory.md) explains these primitives, transports and
client/server composition. The [practice notebook](02_mcp/02_mcp-practice.ipynb)
connects them to the runnable examples.

## Why Skills complement MCP

A tool exposes an operation. A Skill explains how to perform a task well: when to
use particular operations, in which order, which constraints matter, and how to
verify the result. It can include instructions, reference material and scripts.

For a repository review, a GitHub MCP server might expose issue, pull-request and
file operations. A review Skill can add a checklist: identify the change, read
relevant context, verify behavior, prioritize actionable findings, and cite lines.
The two mechanisms solve different parts of the same workflow.

### Progressive disclosure

Skill-capable hosts typically discover metadata first, load the relevant instructions
when selected, and read supporting resources only when necessary. The exact trigger
and loading behavior depend on the host. This can reduce irrelevant context, but
token savings are workload-dependent. A comparison such as 16,000 versus 500 tokens
is an illustration, not a guaranteed benchmark.

Good metadata makes the trigger clear. Good instructions explain the workflow.
Scripts handle deterministic or repetitive operations that prose alone cannot execute.
Separate large references so they can be loaded selectively, and avoid hiding required
steps behind an undocumented file.

### Minimal Skill layout

```text
w-openweather/
  SKILL.md
  scripts/
    weather.py
```

```yaml
---
name: w-openweather
description: Query current weather or forecasts through the bundled OpenWeather CLI.
---
```

The body documents setup, arguments, execution and interpretation. Write descriptions
around user intent, including relevant exclusions. Do not promise capabilities that
the scripts do not implement. Optional host-specific metadata is not universally portable.

## Comparing the three approaches

| Approach | What it packages | Runtime responsibility | Useful when |
| --- | --- | --- | --- |
| Function Calling | Function name and argument schema | Validate and execute model requests | Teaching or a small application with direct functions |
| MCP | Discoverable protocol capabilities | Maintain client/server connections and host policy | Sharing tools across compatible hosts |
| Skill | Task instructions, references and optional scripts | Load instructions and execute available operations | Reusable task procedures and local automation |

The weather case implements the same OpenWeather operation through both
[MCP](02_mcp/mcp/01_weather-mcp-server/README.md) and a
[Skill](03_skills/cases/01_weather_skill/README.md). The Skill invokes its own CLI;
it does not call the MCP server. Both support English and Chinese output, and both
depend on an OpenWeather key for real queries.

Use the simplest integration that matches the task. Add a service when shared
protocol access is useful, and a Skill when the repeatable procedure itself carries
value. Read the [Skill theory](03_skills/skills-theory.md) for design and evaluation.
