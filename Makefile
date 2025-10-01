# Makefile

.PHONY: help buildenv lab research test docs docs-serve lint clean
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

ensure-uv:
	@echo "+++ $@"
	@if ! command -v uv > /dev/null; then \
		echo "uv not found, installing with sudo pip install uv..."; \
		sudo pip install uv; \
	fi

uv.lock: pyproject.toml ensure-uv
	@echo "+++ $@"
	uv lock

.venv/bin/activate: uv.lock
	@echo "+++ $@"
	uv venv
	uv sync --all-extras
	@touch $@

buildenv: .venv/bin/activate ## Create build environment
	@echo "+++ $@"
	
lab: buildenv ## Edit welltrack-lab.py in marimo
	@echo "+++ $@"
	. .venv/bin/activate && marimo edit scripts/welltrack-lab.py

test: buildenv ## Run Tests
	@echo "+++ $@"
	mkdir -p build/test

build/site/index.html:
	mkdir -p build/site
	. .venv/bin/activate && mkdocs build -f mkdocs.yml

docs-mkdocs: build/site/index.html

build/wheel/welltrack_lab-0.1.0-py3-none-any.whl:
	mkdir -p build/wheel
	. .venv/bin/activate && python -m build --wheel --installer uv -o build/wheel

docs-wheel: build/wheel/welltrack_lab-0.1.0-py3-none-any.whl

build/site/marimo/index.html: docs-wheel
	mkdir -p build/notebooks/public
	cp build/wheel/welltrack_lab-*-py3-none-any.whl build/notebooks/public
	cp scripts/welltrack-lab.py build/welltrack-lab/
	. .venv/bin/activate && printf "y\n" | marimo export html-wasm \
		build/welltrack-lab/welltrack-lab.py -o build/site/marimo --mode run

docs-marimo: build/site/marimo/index.html

docs: buildenv docs-mkdocs docs-wheel docs-marimo ## Make Documentation and Onlinepage
	@echo "+++ $@"

docs-serve: docs ## Serve Documentation locally
	@echo "+++ $@"
	. .venv/bin/activate && scripts/dev_serve.py -d build/site


lint: buildenv ## Run Linting
	@echo "+++ $@"
	. .venv/bin/activate && flake8 \
		. --exclude .git,__pycache__,build,.venv \
		--select=E9,F63,F7,F82 --show-source --statistics
	. .venv/bin/activate && flake8 \
		. --exclude .git,__pycache__,build,.venv \
		--count --exit-zero --max-complexity=10 \
		--max-line-length=95 --statistics \
		--output-file build/test/flake8.txt

clean: ## Remove test and build artifacts
	@echo "+++ $@"
	rm -rf .venv __marimo__ .pytest_cache build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	for i in uv.lock; do if test -e "$$i"; then rm "$$i"; fi; done
