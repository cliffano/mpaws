# AGENTS.md

This repository contains a Python project following a unified standard for tooling, build automation, and coding conventions. All projects share the same tooling stack and conventions to ensure consistency and maintainability.

The key components of the standard include:

- Build automation (PieMaker)
- Project definition and dependency management (Poetry)
- Code formatting (Black)
- Static analysis (Pylint)
- Testing (Pytest)

This document outlines the common conventions that apply across the Python projects.

## Python Version & Dependencies

- **Python Version**: 3.10+
- **Dependency Manager**: Poetry
- **Lock File**: `poetry.lock` (checked in)
- **Dependency Specification**: `pyproject.toml` (Poetry format)

### Adding Dependencies

```bash
poetry add package_name          # Add to runtime deps
poetry add --group dev pkg_name  # Add to dev deps
make deps                        # Install all deps
```

### VirtualEnv

- **Virtual environment**: `.venv/` (Poetry-managed)
- **PATH prefix**: `.venv/bin:` (binaries available as `pylint`, `black`, `pytest`, etc.)

### Project Structure

```text
project/
├── <module>                  # Main package
│   ├── __init__.py
│   ├── logger.py
│   └── ...
├── examples/                 # Example configs and usage
├── tests/                    # Unit tests
├── tests-integration/        # Integration tests
├── docs/                     # Generated documentation
├── stage/                    # Temporary stage files
├── .coveragerc               # Coverage configuration
├── .github/                  # GitHub workflows
├── .gitignore                # Git ignore rules
├── .pylintrc                 # Pylint configuration
├── .rtk.json                 # RTK configuration
├── .venv/                    # Virtual environment (Poetry-managed)
├── AGENTS.md                 # Agent instructions (this file)
├── avatar.jpg                # Project avatar (80x80 pixels)
├── CHANGELOG.md              # Changelog file following Keep a Changelog format
├── LICENSE                   # License file
├── Makefile                  # Build automation (PieMaker)
├── piemaker.yml              # PieMaker configuration
├── poetry.lock               # Locked dependencies
├── pyproject.toml            # Poetry configuration
├── README.md                 # Project README
└── requirements.txt          # Python dependencies generated from Poetry
```

## Build Automation (PieMaker)

This Python project uses **PieMaker** as a standard build automation tool that unifies the build pipeline across all Python projects.

### Common Commands

```bash
make ci                # Run full CI pipeline
make all               # Alias for ci
make clean             # Remove temporary, staged, cached files using rm
make stage             # Create stage directory using mkdir
make deps              # Install dependencies using Poetry
make deps-upgrade      # Upgrade dependencies to latest versions using poetry-plugin-up
make rmdeps            # Remove dependency files (`.venv`, `poetry.lock`, `requirements.txt`) using rm
make style             # Check/format code using Black
make lint              # Run static analysis using Pylint
make test              # Run unit tests using Pytest
make test-examples     # Run example shell scripts using bash
make coverage          # Generate coverage reports using coverage.py and unittest
make complexity        # Run complexity analysis using Radon
make doc               # Generate documentation using Sphinx (sphinx-apidoc + make html)
make package           # Build package using Poetry
make install           # Install package into virtual environment using Poetry
make uninstall         # Uninstall package using pip
make reinstall         # Reinstall package using pip + Poetry (`uninstall` then `install`)
make test-integration  # Run integration tests using Pytest
```

### Release Targets

```bash
make release-major     # Create major release using RTK
make release-minor     # Create minor release using RTK
make release-patch     # Create patch release using RTK
```

### Update Targets

```bash
make update-to-latest  # Update Makefile to latest PieMaker tag using curl + GitHub API + jq
make update-to-main    # Update Makefile to PieMaker main branch using curl
make update-to-version # Update Makefile to specific PieMaker version using curl
make update-dotfiles   # Refresh project dotfiles using generator-python (git clone + plop + cp)
```

## Development Environment

This project is designed to be developed in a consistent environment via Docker image `cliffano/studio`.

You can run the container using: `docker run --rm --workdir /opt/workspace -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/opt/workspace -i -t cliffano/studio` and then run the build commands inside the container.

Alternatively you can run the PieMaker Makefile targets via Docker container entrypoint, e.g. `docker run --rm --workdir /opt/workspace -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/opt/workspace -i -t cliffano/studio make ci`.

## Code Style and Linting

Applies to: `**/*.py`

- Formatting uses Black via `make style`
- Static analysis uses Pylint via `make lint`

### Style & Formatting

#### Black Formatter

All code must pass `black` formatting:

```bash
make style  # Via PieMaker
```

**Guidelines**:

- Use double quotes for strings (Black default)
- Don't manually format — `black` is authoritative
- Line length: 88 characters max

#### Pylint Static Analysis

All code should have zero Pylint error and warning:

```bash
make lint
```

**Guidelines**:

- Disable warnings only when justified: `# pylint: disable=missing-docstring`
- Use specific codes, not blanket disables when the exemptions are only specific lines
- Attempt to fix warning root causes before disabling

### Python Conventions

#### Imports

- Standard library imports first
- Third-party imports second (organized alphabetically)
- Local imports last
- Blank line between groups

```python
from typing import Dict, List
from unittest.mock import MagicMock, patch

import yaml

from mymodule import MyClass
from mymodule.utils import helper_function
```

#### Type Hints

Use type hints where appropriate:

```python
def process_items(config_file: str, batch_size: int) -> None:
    """Process items from configuration file in batches."""
    ...

def _format_output(data: dict) -> str:
    """Format data to output string format."""
    ...
```

#### Docstrings

Use **Google-style** or **Sphinx-style** docstrings depending on the module context:

**Google style (preferred for `__init__` methods)**:

```python
def __init__(self, config: dict):
    """Initialize service with configuration.

    Args:
        config: Configuration dictionary with required keys.

    Raises:
        ValueError: If configuration is invalid.
    """
    ...
```

**Sphinx style (for complex methods)**:

```python
def process_batch(self, items: list, batch_size: int = 50) -> None:
    """Process a batch of items.

    :param items: List of items to process.
    :param batch_size: Number of items per batch (default: 50).
    :raises IOError: If processing fails.
    """
    ...
```

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `DataProcessor`, `TestDataParser`)
- **Functions/Methods**: `snake_case` (e.g., `process_data`, `_format_output`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_BATCH_SIZE`)
- **Private/Internal**: Prefix with `_` (e.g., `_internal_helper`, `_format_error`)
- **Variables**: `snake_case` (e.g., `result_dict`, `item_count`)

#### Logging

Always use a logger via Conflog, never print.

Have a logger instance in each module:

```python
from conflog import Conflog

LOGGER = None

def init():
    """Initialize logger.

    Logger is cached to prevent duplicate handlers
    from being added on repeated calls.
    """

    global LOGGER  # pylint: disable=global-statement
    if LOGGER is not None:
        return LOGGER

    cfl = Conflog(
        conf_dict={"level": "info", "format": "[<module>] %(levelname)s %(message)s"}
    )

    LOGGER = cfl.get_logger(__name__)
    return LOGGER
```

Then use the logger for all output:

```python
from .logger import init

logger = init(__name__)

logger.info("Message with %s", variable)
logger.error("Error message")
logger.debug("Debug message")
```

**Guidelines**:

- Use `%s` format placeholders, not f-strings, in logger calls
- Pass variables as separate arguments: `logger.info("msg %s", var)` not `logger.info(f"msg {var}")`
- f-strings are avoided within logger calls to prevent unnecessary string interpolation when the log level is higher than the message level
- Info level for important operations, debug for internal flow and troubleshooting

### File Organization

#### Module Structure

```python
# 1. Module docstring
"""Module description and purpose."""

# 2. Imports
from typing import Dict
import yaml

# 3. Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# 4. Classes
class MyClass:
    """Class docstring."""
    ...

# 5. Functions
def my_function():
    """Function docstring."""
    ...

# 6. CLI or main entry (if applicable)
def cli():
    ...
```

#### Line Length

- **Code**: 88 characters (Black standard)
- **Docstrings/comments**: 79 characters (PEP 257)
- **URLs/long strings**: Acceptable to exceed if no reasonable break

### Error Handling

#### Use Exceptions, Not Exit Codes

```python
# Good
raise IOError(f"Config file not found: {file_path}")

# Avoid
print("ERROR: Config file not found")
sys.exit(1)
```

#### Let Exceptions Propagate

Let the caller handle exceptions unless you're adding context:

```python
# Good
try:
    result = perform_operation(data)
except Exception as e:
    logger.error("Operation failed: %s", str(e))
    raise

# Avoid
try:
    result = perform_operation(data)
except Exception:
    pass  # Silent failure
```

### Common Patterns

#### Reading Configuration

Always load configuration file using cfgrw:

```python
from cfgrw import CFGRW

def load_config(conf_file: str) -> dict:
    """Load configuration from file."""
    config = CFGRW(conf_file=conf_file).read(["key1", "key2"])
    return config
```

#### Mocking Dependencies in Tests

Patch where the dependency is **used**, not where it's defined:

```python
# Good: Patch in the module where the dependency is used
@patch("mymodule.service.ExternalAPI")  # Imported in service.py
def test_operation(self, mock_api_cls):
    ...

# Avoid: Patching at the origin
@patch("external_library.API")  # Generic library module
def test_operation(self, mock_api_cls):
    ...
```

### Avoid

- **Bare `except:`** - Always catch specific exceptions
- **Global state** - Pass dependencies as arguments
- **Mutable default arguments** - Use `None` and create new instance
- **Over-nesting** - Extract functions if indentation gets deep (>3 levels)
- **Silent failures** - Log errors before continuing

## Testing

Applies to: `tests/**/*.py`, `tests-integration/**/*.py`

- Unit tests live in `tests/`
- Integration tests live in `tests-integration/`
- Run tests with `make test` and `make test-integration`

### Test Structure

#### Unit Tests

**Location**: `tests/test_*.py`

**Purpose**: Test individual functions/methods in isolation

**Scope**:

- No filesystem and network calls (mock them)
- Faster execution
- High code coverage

#### Integration Tests

**Location**: `tests-integration/test_*.py`

**Purpose**: Test end-to-end flows with real or semi-real external systems

**Scope**:

- May use filesystem and network calls (with test fixtures or mocks if needed)
- Slower execution
- Broader coverage (fewer, larger tests)

#### Test Files

```text
tests/
  test_module1.py        # Tests for module1.py
  test_module2.py        # Tests for module2.py
  test_utils.py          # Tests for utils.py

tests-integration/
  test_cli.py            # Integration tests for CLI
  test_service.py        # Integration tests for main service
```

#### Test Classes

```python
class TestDataProcessor(unittest.TestCase):
    """Tests for DataProcessor class."""
    ...

class TestFormatOutput(unittest.TestCase):
    """Tests for _format_output method."""
    ...
```

#### Test Methods

```python
def test_single_item_success(self):
    """Test processing a single item successfully."""
    ...

def test_operation_failure_logs_error(self):
    """Test that operation failure logs an error."""
    ...

def test_batching_over_max_size(self):
    """Test that items are batched when count exceeds max."""
    ...
```

**Pattern**: `test_<description_of_scenario>`

### Pytest Execution

#### Running Tests

```bash
# All tests
make test

# All tests (quick mode)
pytest -q

# Specific file
pytest tests/test_module.py

# Specific test
pytest tests/test_module.py::TestClass::test_method

# Test matching a keyword
pytest -k "batch" -v
```

#### Configuration

- Framework: `pytest`
- No special fixtures needed (use `unittest.TestCase` directly)
- Coverage: `pytest-cov` (via `make coverage`)

### Mocking Best Practices

#### Import Mocking

```python
from unittest.mock import MagicMock, patch
```

#### Patch at the Usage Point

Always patch where the dependency is imported/used:

```python
# Good: Patch in the module where dependency is used
@patch("mymodule.service.ExternalAPI")
def test_operation(self, mock_api_cls):
    ...

# Avoid: Patching at the origin
@patch("external_library.API")
def test_operation(self, mock_api_cls):
    ...
```

#### Mock Structure

```python
# Create mocks
mock_api = MagicMock()
mock_logger = MagicMock()

# Set return values
mock_api.execute.return_value = mock_result

# Use in test
...

# Assert calls
mock_api.execute.assert_called_once()
assert mock_logger.info.call_count == 2
```

#### Mocking File I/O

```python
with patch("builtins.open", mock.mock_open(read_data="config data")):
    result = read_config_file("config.yaml")
```

#### Mocking External Services

```python
with patch("mymodule.service.ExternalAPI") as mock_api_cls:
    mock_api = MagicMock()
    mock_api_cls.return_value = mock_api
    mock_api.execute.return_value = MagicMock(status="ok", data="result")

    service = MyService({"url": "http://localhost:8080", "user": "u", "token": "t"})
    # Test code
```

### Test Assertion Patterns

#### Basic Assertions

```python
# Value equality
assert result == expected_dict

# Membership
assert "field" in result
assert key not in result

# Type checking
assert isinstance(result, dict)
assert callable(func)

# Boolean
assert result is None
assert result is not None
```

#### Mock Assertions

```python
# Called once with no args
mock_func.assert_called_once()

# Called with specific args
mock_func.assert_called_once_with("arg1", "arg2")

# Not called
mock_func.assert_not_called()

# Call count
assert mock_func.call_count == 3

# Call arguments
assert mock_func.call_args[0] == ("arg1",)
assert mock_func.call_args.kwargs == {"key": "value"}

# All calls
for call in mock_func.call_args_list:
    print(call)
```

#### Logger Assertions

```python
# Check logger was called
mock_logger.info.assert_called_once_with("Operation %s completed", "task")

# Check error was logged
mock_logger.error.assert_called_once()

# Check call arguments
error_msg = mock_logger.error.call_args[0][0]
```

### Unit Test Patterns

#### Testing a Simple Function

```python
def test_format_output_required_fields_only(self):
    """Test output formatting with required fields only."""
    input_data = {
        "name": "Item",
        "status": "active",
        "value": 42,
    }
    result = format_output(input_data)

    assert result["name"] == "Item"
    assert result["status"] == "active"
    assert result["value"] == 42
```

#### Testing a Method with External Dependency

```python
@patch("mymodule.service.ExternalAPI")
@patch("mymodule.logger.init")
def test_operation_success(self, mock_init, mock_api_cls):
    """Test successful operation with external API."""
    # Setup
    mock_logger = MagicMock()
    mock_init.return_value = mock_logger

    mock_api = MagicMock()
    mock_api_cls.return_value = mock_api
    mock_result = MagicMock(status="success", value="result_data")
    mock_api.execute.return_value = mock_result

    # Execute
    config = {"url": "http://localhost", "user": "user", "token": "token"}
    service = MyService(config)
    output = service.perform_operation({"input": "data"})

    # Assert
    mock_logger.info.assert_called_once_with("Operation completed: %s", "result_data")
```

### Integration Test Patterns

#### Testing CLI with CliRunner

```python
from click.testing import CliRunner
from mymodule import cli

def test_cli_help():
    """Test CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
```

#### Testing Constructor Error Paths

```python
def test_constructor_with_missing_config(self):
    """Test service constructor with missing config file."""
    from cfgrw import CFGRW
    from mymodule.service import MyService

    with pytest.raises(FileNotFoundError):
        config = CFGRW(conf_file="nonexistent.yaml").read(...)
        service = MyService(config)
```

### Coverage

#### Generate Coverage Report

```bash
make coverage
```

#### Coverage Goals

- Aim for >= 90% code coverage
- Focus on critical paths (success flows, error handling)
- Be pedantic and don't ignore trivial getters/setters

### Common Pitfalls

1. **Mocking at the wrong level** - Patch where used, not imported
2. **Not resetting mocks** - Use `reset_mock()` between assertions
3. **Hardcoding test data** - Use descriptive variable names
4. **Not testing edge cases** - Empty lists, None values, exceptions
5. **Over-testing** - Test behavior, not implementation details
6. **Flaky tests** - Mock time-based logic, remove random delays

### CI Integration

Tests are run as part of `make ci`:

```bash
make test              # Unit tests
make test-integration  # Integration tests
```

All tests must pass before merging.

## Documentation

- Documentation is generated with Sphinx via `make doc`
- Generated outputs live under `docs/`

Common generated subdirectories under `docs/`:

- `doc/` for generated API documentation
- `coverage/` for coverage reports
- `complexity/` for complexity analysis reports
- `lint/` for lint reports
- `test/` for unit test reports
- `test-integration/` for integration test reports

## Continuous Integration Pipeline

The Makefile (PieMaker) orchestrates standard build targets, with `make ci` running the following steps in sequence:

- clean              # 1. Clean temp files
- deps               # 2. Install dependencies
- style              # 3. Format & check code (black)
- lint               # 4. Static analysis (pylint)
- test               # 5. Unit tests (pytest)
- coverage           # 6. Coverage reports
- complexity         # 7. Complexity analysis
- doc                # 8. Generate documentation
- package            # 9. Build distribution
- reinstall          # 10. Clean install from package
- test-integration   # 11. Integration tests

All steps must pass before code is merged. Developers should run `make ci` locally before pushing to ensure the CI pipeline will pass.

After the code is merged, the CI pipeline will run as Github CI workflow.

### Common Commit Message Patterns

Use clear, imperative commit messages:

- `Fix test patch paths by avoiding command/module name collisions`
- `Add unit tests for blur-plates module`
- `Update README and example script to use categorise-orientation`
- `Remove deprecated blur-plates module and related code`

## GitHub Workflows

This repository defines the following workflows under `.github/workflows/`:

- **CI** (`ci-workflow.yaml`): Trigger: `push`, `pull_request`, and manual `workflow_dispatch`. Purpose: Runs the full quality pipeline (`make ci`) across a Python version matrix (usually LTS versions), runs example tests, and publishes generated docs to GitHub Pages.

- **CodeQL** (`codeql-analysis.yml`): Trigger: `push` to `main`, `pull_request` targeting `main`, and weekly scheduled run (`cron`). Purpose: Performs GitHub CodeQL static security analysis for Python and uploads code scanning results.

- **Publish** (`publish-workflow.yaml`): Trigger: `push` of any Git tag. Purpose: Builds and installs the package, then publishes it using `make publish`.

- **Release Major** (`release-major-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Creates a major release via `cliffano/release-action` (`release_type: major`).

- **Release Minor** (`release-minor-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Creates a minor release via `cliffano/release-action` (`release_type: minor`).

- **Release Patch** (`release-patch-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Creates a patch release via `cliffano/release-action` (`release_type: patch`).

- **Upgrade Deps** (`upgrade-deps-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Upgrades dependencies, runs the main validation/build targets, commits dependency updates, and pushes changes back to the current branch.
