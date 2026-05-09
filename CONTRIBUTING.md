# Contributing

## Project structure

```
audl/
├── audl/
│   ├── stats/
│   │   ├── endpoints/       # One module per data source (PlayerProfile, GameStats, etc.)
│   │   ├── library/         # Shared helpers (game_event.py, parameters.py)
│   │   └── static/          # Constants (e.g. FIRST_SEASON_YEAR)
│   └── utils/               # General-purpose utilities (players.py)
├── tests/
│   └── stats/
│       └── endpoints/       # Unit tests mirroring the endpoints structure
├── examples/                # Jupyter notebooks with worked examples
├── docs/                    # Auto-generated HTML docs (pdoc3)
├── makefile
├── requirements.txt
└── setup.py
```

Each endpoint in `audl/stats/endpoints/` inherits from `_base.py` and is responsible for fetching and returning data as a pandas DataFrame. When adding a new data source, follow the same pattern: subclass `Endpoint`, implement `_get_url()`, and expose results through public `get_*()` methods.

## Setting up the environment

```bash
git clone https://github.com/yukikongju/audl.git
cd audl
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Install the pre-commit hooks (runs Black and other checks automatically on each commit):

```bash
make precommit_hook
# or equivalently:
pre-commit install
```

## Running the tests

Tests use `unittest` and live in `tests/stats/endpoints/`. Each endpoint has a corresponding test file.

Run all tests:

```bash
python3 -m pytest tests/
```

Run tests for a specific endpoint:

```bash
python3 -m pytest tests/stats/endpoints/test_gamestats.py
```

Note: the tests make live HTTP requests to the AUDL stats API, so an internet connection is required.

## Code style

This project uses [Black](https://black.readthedocs.io/) for formatting (line length 80) and enforces it via pre-commit. Before opening a PR, make sure your code is formatted:

```bash
black --line-length 80 audl/ tests/
```

## Submitting changes

This project uses [Conventional Commits](https://www.conventionalcommits.org/) enforced via [Commitizen](https://commitizen-tools.github.io/commitizen/). Use `cz commit` instead of `git commit` to be guided through the format:

```bash
cz commit
# or:
make commitizen_commit
```

Common commit types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

**Workflow:**

1. Fork the repository and create a branch from `master`.
2. Make your changes and add tests for any new behaviour.
3. Run the test suite and confirm everything passes.
4. Push your branch and open a pull request against `master`.
5. Describe what the change does and why in the PR description.

## Generating docs

The HTML documentation is generated with [pdoc3](https://pdoc3.dev/) from docstrings:

```bash
make docs
```

The output is written to `docs/`. If you add or modify public methods, update their docstrings accordingly.

## Reporting bugs

Open an issue on [GitHub Issues](https://github.com/yukikongju/audl/issues) and include:

- A short description of the unexpected behaviour
- The endpoint or method involved
- A minimal code snippet that reproduces the problem
- The full error traceback, if applicable
- Your Python version and `audl` version (`pip show audl`)
