# Contributing

Thanks for your interest in contributing! Here's how to get started.

## Setup

1. Fork the repo and clone locally
2. Create a virtualenv and install deps:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. Copy `.env.example` → `.env` and fill in your values

## Development Workflow

- Create a feature branch: `git checkout -b feature/my-change`
- Write tests for new functionality
- Run the test suite: `pytest tests/ -v`
- Lint your code: `flake8 app/ && mypy app/`
- Open a pull request with a clear description

## Code Style

- Follow PEP 8
- Use type hints wherever possible
- Write docstrings for all public functions
- Use the project logger (`from app.utils.logger import logger`) instead of `print()`

## Reporting Issues

Open a GitHub issue with:
- Steps to reproduce
- Expected vs. actual behaviour
- Environment details (OS, Python version)
