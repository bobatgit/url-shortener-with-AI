.PHONY: help install install-dev test lint format clean run run-dev deploy

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests with pytest"
	@echo "  lint         Run code quality checks"
	@echo "  format       Format code with black and isort"
	@echo "  clean        Remove generated files"
	@echo "  run          Run production server"
	@echo "  run-dev      Run development server"
	@echo "  deploy       Deploy application to production"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

test:
	./scripts/run_tests.sh

lint:
	flake8 app tests
	mypy app tests
	black --check app tests
	isort --check-only app tests

format:
	black app tests
	isort app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

run:
	./scripts/deploy.sh

run-dev:
	./scripts/dev.sh

deploy:
	./scripts/deploy.sh