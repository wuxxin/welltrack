# Makefile

.PHONY: help buildenv test lab docs sample-data dev-serve dev-serve-ssl lint clean clean-all
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
	uv venv --clear
	uv sync --all-extras --all-groups
	. .venv/bin/activate && playwright install chromium-headless-shell
	@touch $@

buildenv: .venv/bin/activate ## Create build environment
	@echo "+++ $@"
	
lab: buildenv ## Edit welltrack-lab.py in marimo
	@echo "+++ $@"
	. .venv/bin/activate && marimo edit scripts/welltrack-lab.py

test: docs build/tests/sample-data.json ## Create Sample Data, run Tests
	@echo "+++ $@"
	mkdir -p build/tests/output
	. .venv/bin/activate && pytest --screenshot on --video retain-on-failure --output build/tests/output tests/

sample-data: build/tests/sample-data.json ## Create build/tests/sample-data.json
	@echo "+++ $@"

build/tests/sample-data.json: buildenv scripts/create-sample-data.py
	mkdir -p build/tests
	. .venv/bin/activate && scripts/create-sample-data.py build/tests/sample-data.json

build/site/index.html:
	mkdir -p build/site
	. .venv/bin/activate && mkdocs build -f mkdocs.yml

docs-mkdocs: build/site/index.html
	@echo "+++ $@"

build/site/welltrack/welltrack.html: docs-mkdocs
	mkdir -p build/site/welltrack
	cp src/welltrack/* build/site/welltrack

docs-welltrack-app: build/site/welltrack/welltrack.html
	@echo "+++ $@"

build/site/prototypes/audio-gps-logging.html: docs-mkdocs
	mkdir -p build/site/prototypes
	cp dev/prototypes/* build/site/prototypes

docs-prototypes: build/site/prototypes/audio-gps-logging.html
	@echo "+++ $@"

build/wheel/welltrack_lab-0.1.0-py3-none-any.whl:
	mkdir -p build/wheel
	. .venv/bin/activate && python -m build --wheel --installer uv -o build/wheel

docs-wheel: build/wheel/welltrack_lab-0.1.0-py3-none-any.whl
	@echo "+++ $@"

build/site/marimo/index.html: docs-wheel
	mkdir -p build/welltrack-lab/public
	cp build/wheel/welltrack_lab-*-py3-none-any.whl build/welltrack-lab/public
	cp scripts/welltrack-lab.py build/welltrack-lab/
	. .venv/bin/activate && printf "y\n" | marimo export html-wasm \
		build/welltrack-lab/welltrack-lab.py -o build/site/marimo --mode run

docs-marimo: build/site/marimo/index.html
	@echo "+++ $@"

docs: buildenv docs-mkdocs docs-welltrack-app docs-prototypes docs-wheel docs-marimo ## Make Onlinepage and WebApp
	@echo "+++ $@"

dev-serve-ssl: docs ## HTTPS Serve Documentation on port 8443
	@echo "+++ $@"
	. .venv/bin/activate && scripts/dev_serve.py -d build/site 8443

dev-serve: docs ## HTTP Serve Documentation on port 8000
	@echo "+++ $@"
	. .venv/bin/activate && python -m http.server -d build/site 8000

lint: buildenv ## Run Linting
	@echo "+++ $@"
	mkdir -p build/tests
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
	rm -rf __marimo__ .pytest_cache build
	find . -type d -name "__pycache__" -exec rm -rf {} +

clean-all: clean ## Remove environment and all artifacts
	@echo "+++ $@"
	rm -rf .venv
	for i in uv.lock; do if test -e "$$i"; then rm "$$i"; fi; done
