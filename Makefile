package_version := $(shell python -c "from package import version; print(version)")

check:
	@echo "Checking backend..."
	uv version $(package_version)
	uv run ruff check server --fix
	uv run ruff format server
	uv run mypy server/


build: check
	python create_package.py
