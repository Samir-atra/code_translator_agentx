# Code Translator AgentX

Code Translator AgentX is a multi-agent evaluation framework built on the [Agent-to-Agent (A2A) protocol](https://a2a-protocol.org/) and [Google ADK](https://google.github.io/adk-docs/). It orchestrates competitive coding scenarios where autonomous agents translate code between programming languages, subject to rigorous evaluation by an expert judge agent.

## Technical Architecture

The system follows a Green/Purple agent architecture:

### 1. Evaluator Agent (Green Agent)
**Implementation**: `src/scenarios/code_translator/adk_translator_judge.py`
**Model**: `gemini-2.5-flash`

The Evaluator acts as the orchestration host and final judge. It performs the following technical functions:
*   **Orchestration**: Manages the A2A task lifecycle, synchronizing interactions between participants.
*   **Validation**: Ensures evaluation requests adhere to the `EvalRequest` schema.
*   **Scoring Engine**: Implements a multi-dimensional scoring rubric via `TranslatorJudgeADK`:
    *   **Execution Correctness**: Verification of runnable code without errors.
    *   **Style & Documentation**: Adherence to language-specific conventions and commenting standards.
    *   **Conciseness**: Avoidance of redundant boilerplate.
    *   **Logic Preservation**: Structural and logical equivalence to the source.
*   **Output**: Structured `TranslatorEval` JSON artifacts detailing scores and declaring a winner.

### 2. Participant Agents (Purple Agents)
**Implementation**: `src/scenarios/code_translator/translator.py`
**Model**: `gemini-2.5-flash`

The system currently supports two distinct participant roles defined in `translator_scenario.toml`:
*   `researcher_translator`
*   `developer_translator`

These agents are instantiated as Google ADK `Agent` objects, exposing an A2A-compliant HTTP server via `uvicorn`. They accept translation tasks and stream responses back to the evaluator.

## Installation & Setup

### Prerequisites
*   Python 3.11+
*   [uv](https://github.com/astral-sh/uv) (for local execution)
*   Docker (for containerized execution)
*   Google GenAI API Key

### Configuration
1.  Clone the repository.
2.  Copy the sample environment file and add your API key:
    ```bash
    cp sample.env .env
    # Edit .env and set GOOGLE_API_KEY
    ```

## Execution Modes

### 1. Docker (Recommended)

The project includes a production-ready Docker setup leveraging multi-stage builds and strict layer caching.

**Build the Image:**
```bash
docker build -f docker/Dockerfile -t samiratra95/code_translator_agentx .
```

**Run the Scenario:**
Pass your environment variables directly to the container:
```bash
docker run --rm -it --env-file .env samiratra95/code_translator_agentx \
    agentbeats-run scenarios/code_translator/translator_scenario.toml
```

**Alternative: Mount .env file**
If you prefer mounting the file (useful for rapid config changes):
```bash
docker run --rm -it -v $(pwd)/.env:/app/.env samiratra95/code_translator_agentx
```

### 2. Local Execution

Run the agents and orchestrator directly on your host machine.

**Install Dependencies:**
```bash
uv sync
```

**Run Scenario:**
```bash
uv run agentbeats-run scenarios/code_translator/translator_scenario.toml
```

## Project Structure

```
├── docker/
│   ├── Dockerfile              # Multi-stage Docker build definition
│   └── .dockerignore           # Build context exclusion rules
├── scenarios/
│   └── code_translator/
│       ├── adk_translator_judge.py    # Green Agent (Evaluator) implementation
│       ├── translator.py              # Purple Agent (Participant) implementation
│       ├── translator_judge_common.py # Shared Pydantic models & types
│       └── translator_scenario.toml   # Scenario configuration (ports, roles)
├── src/
│   └── agentbeats/             # Core A2A execution primitives
└── pyproject.toml              # Dependency management
```
