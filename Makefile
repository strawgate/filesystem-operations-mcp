

.PHONY: help install update-deps uv-sync activate build check test test-smoke clean clean-full lint autocorrect format inspector

help:
	@echo "Dependency Management:"
	@echo "  setup         - Set up the virtual environment and install dependencies"
	@echo "  update-deps   - Update dependencies"
	@echo "  uv-sync       - Create uv lockfile"

	@echo "Build and Check:"
	@echo "  check         - Run linting and tests"

	@echo "Testing:"
	@echo "  test          - Run unit tests"

	@echo "Cleaning:"
	@echo "  clean-full    - Clean up all including virtual environment"
	@echo "  - clean       - Clean up cache and temporary files"

	@echo "Linting:"
	@echo "  lint                - Run format and autocorrect"
	@echo "  - lint-autocorrect  - Run ruff check --fix"
	@echo "  - lint-format       - Run ruff format"

	@echo "Helpers:"
	@echo "  inspector     - Run MCP Inspector"

uv-sync:
	@echo "Running uv sync..."
	uv sync
	uv sync --extra dev

check: lint test test-smoke

test:
	@echo "Running pytest..."
	uv run pytest

inspector:
	@echo "Running MCP Inspector..."
	npx @modelcontextprotocol/inspector
lint: autocorrect format

autocorrect:
	@echo "Running ruff check --fix..."
	uv run ruff check . --fix

format:
	@echo "Running ruff format..."
	uv run ruff format .

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__ **/__pycache__
	rm -rf .pytest_cache **/.pytest_cache
	rm -rf .ruff_cache **/.ruff_cache
	rm -rf **/.pyc
	rm -rf **/.pyo

clean-full: clean
	@echo "Cleaning up all..."
	rm -rf .venv

update-deps:
	@echo "Updating dependencies..."
	uv sync -U


setup:
	@echo "Setting up environment..."
	python3 -m venv .venv
	uv sync
	uv sync --dev
	echo "Activate the environment with 'source .venv/bin/activate'"
