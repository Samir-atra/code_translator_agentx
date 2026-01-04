FROM python:3.11-slim-bookworm

# Install uv by copying it from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen: sync based on uv.lock
# --no-install-project: install only dependencies for better layer caching
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Install the project itself
RUN uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Default command - can be overridden
CMD ["agentbeats-run", "--help"]
