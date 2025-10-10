# Project Development Documentation

## Files and Directories Layout

### Development Documents

- `dev/system-workflow.md`: Development process and coding conventions.
- `dev/product-requirements.md`: High-level functional and non-functional requirements.
- `dev/development.md`: (This file) The project file layout, architectural overview and developer guidelines for working with project.
- `dev/marimo-development.md`: Developer Guidelines for working with marimo notebooks of this project.
- `dev/product-specifications.md`: Low-Level functional and non-functional specifications.
- `dev/tasks.md`: A living document tracking already completed and new to be done tasks.

### User Documentation

- `README.md`: A user centric view on howto use the app. It is the primary source of user documentation and should be kept in sync with new features, including adding new sections and placeholders for screenshots. The README.md is in German. Avoid using formal personal pronouns like 'Sie' or 'Du' 'ihre' 'ihr' in the documentation, preferring a neutral tone.
- `assets/*.png`: The screenshots mainly used for README.md
- `docs/`: a mostly symlinked directory (including ../README.md and ../assests, and ../src/welltrack/icon*) for mkdocs user documentation generation.

### Main Welltrack Webapp Software and Assets

- `src/welltrack/`:
    - `welltrack.html`: The main application file containing all HTML, CSS, and JavaScript
    - `sw.js`: The service worker for PWA caching and offline capabilities like notifications
    - `manifest.json`: The PWA web app manifest
    - `icon-192.png`: Application icons
    - `icon-512.png`: Application icons

### Welltrack-Lab - Interactive Marimo Python Webapp

- `src/welltrack_lab/`: Welltrack Lab - Python Library and Tools for Welltrack Lab
    - this library will be available for the interactive marimo lab to import, see Makefile
- `scripts/welltrack-lab.py`: Welltrack Lab - Interactive Marimo main file, for work on marimo notebook always read `dev/marimo-development.md`

### Tools

- `scripts/create-sample-data.py`: python script to create example data for welltrack.html to import
- `scripts/dev_serve.py`: python script for https serving a directory (will generate a selfsigned ssl certificate on the fly)

### Build and Config files

- `Makefile`: central make file for building and developing
    - `make` or `make help` for usage
```txt
buildenv             Create build environment
clean                Remove test and build artifacts
clean-all            Remove environment and all artifacts
dev-serve            HTTP Serve Documentation on port 8000
dev-serve-ssl        HTTPS Serve Documentation on port 8443
docs                 Make Onlinepage and WebApp
lab                  Edit welltrack-lab.py in marimo
lint                 Run Linting
sample-data          create build/tests/sample-data.json
test                 Create Sample Data, run Tests
```

- `mkdocs.yml`: mkdocs configuration
    - In mkdocs.yml, file paths in the nav section are relative to the docs directory, not the project root.
- `pyproject.toml`: python dependencies for interactive marimo, testing and mkdocs build
- `build/site/`: mkdocs homepage
- `build/site/wheel/`: welltrack_lab Library as wheel for integration in build/site/marimo
- `build/site/marimo/`: Welltrack-Lab Interactive Mario html wasm page
- `build/site/welltrack/`: Welltrack Main SingePage WebApp page

## Main Welltrack Webapp

- The application is a single-page application (SPA) contained entirely within src/welltrack/welltrack.html.
- The application's UI is in German.
- User prefers long dates to be formatted as 'Weekday Day.Month.Year' in German (e.g., 'Montag 29.9.2025').
- The application uses localStorage for all data storage, making it a client-side-only application with no backend.
- Dependencies like Tailwind CSS, Chart.js, and date-fns are loaded via CDNs.
- Use python playwright for GUI Testing.
- Python scripts related to welltrack data creation/parsing, should read configuration of mood types and body parts directly from src/welltrack/welltrack.html using regex to ensure they are in sync with the main application's settings.
- A data 'slot' for mood or pain is defined as all entries of that type within a 10-minute window, calculated forwards from the first entry in a given subset

### Testing and Verification of Welltrack Webapp with Playwright

- The command to set up the development environment is `make clean-all buildenv`.
- run `make sample-data` to create `build/tests/sample-data.json`. Always use this sample data if the user requests tests with sample data.
- run `make docs` to create `build/site`, which is needed for testing.
- a changed src/welltrack/welltrack.html (or any other file in that directory) that will be tested for a change needs to be build into `build/site/welltrack` which is done by `make docs` which generates the whole `build/site` directory.
- run `make test` creates sample-data,  runs all integrated playwright tests in `tests/`
    - pytest runs with fixtures from `tests/conftest.py`, to start and stop the `dev_server.py` server serving `build/site` and configure the browser for mobile viewport and locale settings.
- to serve the `build/site` files locally, execute `. .venv/bin/activate && python scripts/dev_serve.py -d build/site 8443 > dev_server.log 2>&1 &`. For this project, the built site is served from build/site on port 8443. do not run the dev server if running `pytest` (or make test, which calls pytest), stop a possible running dev_serv.py before, because the pytest tests use the server start/stop fixtures from `tests/testconf.py`.
- for specific playwright gui testing run where every test screenshot is saved unconditionally: `mkdir -p build/tests/output; . .venv/bin/activate pytest --screenshot on --video retain-on-failure --output build/tests/output` and the testfilename.
- create new playwright tests under `tests/`:
    - include the pytest fixtures of `tests/conftest.py`.
    - always use `build/tests/sample-data.json` as sample data, if not requested otherwise.
    - use the default (`build/tests/output/`) path as screenshot and other output dir, unless good reason for other dir.
    - when requested to run "before after" gui tests as part of the procedure, create one screenshot before a change and another after the requested change. create the test file first, then run the test to create the before screenshot to the `build/tests/output/before` directory, then make the change, then create the after screenshot to the `build/tests/output/after` dir.

- In Playwright, to check if a modal has been hidden (i.e., has the 'hidden' class), use expect(locator).to_be_hidden() instead of wait_for_selector('.hidden'), as the latter will time out waiting for a hidden element to become visible.
- In Playwright, element selectors like page.get_by_title() are case-sensitive and must exactly match the attribute value in the HTML.
- For single-page applications, Playwright scripts should avoid using page.reload() after navigation clicks, as this can reset the application state and cause tests to fail. The expect function's built-in wait is sufficient to handle asynchronous rendering.
- When using Playwright to test features that are not initially visible on the page (e.g., at the bottom of a long scroll), use page.screenshot({ full_page: True }) to capture the entire page content for verification.
- When using Playwright's to_have_class assertion, the argument must be a string or a regular expression, not a lambda function. A regular expression like re.compile(r'\bactive\b') can be used to check for the presence of a class.

## Jules Verification of Welltrack Webapp and Welltrack-Lab Marimo with Playwright

- `jules-scratch/verification/*.py` gui playwright verification files should always include the following playwright browser context setup:

```py
# Playwright: setup correct browser context for dev_server.py https and mobile device emulation testing
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    context = browser.new_context(
        ignore_https_errors=True,
        locale="de-DE",
        timezone_id="Europe/Berlin",
        geolocation={"longitude": 48.208359954959, "latitude": 16.3723010569811},
        permissions=["geolocation", "notifications"],
        **p.devices["Pixel 7"],
    )
```

- `jules-scratch/verification/*.py` gui playwright verification files should always use the `build/tests/sample-data.json` data for testing
- do not delete `jules-scratch` directory, before final acknowledge of the user, to let the user see any created files and screenshots for verification.

## Python Style & Conventions

- **Use uv** (the virtual environment and package manager) whenever executing Python commands, including for unit tests.
- **Use `pyproject.toml`** to add or modify dependencies installed during a task execution. as long as there is no version controlled uv.lock, dont add one to the repository
- **Use python_dotenv and load_env()** for environment variables.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- **Use `pytest` for testing**, playwright and pytest-playwright for gui testing.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:

  ```python
  def example():
      """
      Brief summary

      Args:
          param1 (type): Description
      Returns:
          type: Description
      """
  ```

### Python Testing & Reliability

- **Always create unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
    - Include at least:
        - 1 test for expected use
        - 1 edge case
        - 1 failure case
