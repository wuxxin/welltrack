# Project Development Documentation

## Files and Directories Layout

### Development Documents

- dev/system-workflow.md: Development process and coding conventions.
- dev/product-requirements.md: High-level functional and non-functional requirements.
- dev/development.md: (This file) The project file layout, architectural overview and developer guidlines for working with project.
- dev/product-specifications.md: Low-Level functional and non-functional specifications.
- dev/tasks.md: A living document tracking already completed and new to be done tasks.

### User Documentation

- README.md: A user centric view on howto use the app. It is the primary source of user documentation and should be kept in sync with new features, including adding new sections and placeholders for screenshots. The README.md is in German. Avoid using formal personal pronouns like 'Sie' or 'Du' 'ihre' 'ihr' in the documentation, preferring a neutral tone.
- assets/*.png: The screenshots mainly used for README.md
- docs: a mostly symlinked directory (including ../README.md and ../assests, and ../src/welltrack/icon*) for mkdocs user documentation generation.

### Main Welltrack Webapp Software and Assets

- src/welltrack:
    - welltrack.html: The main application file containing all HTML, CSS, and JavaScript
    - sw.js: The service worker for PWA caching and offline capabilities like notifications
    - manifest.json: The PWA web app manifest
    - icon-192.png: Application icons
    - icon-512.png: Application icons

### Welltrack-Lab - Interactive Marimo Python Webapp

- src/welltrack_lab/: Welltrack Lab - Python Library and Tools for Welltrack Lab
    - this library will be available for the interactive marimo lab to import, see Makefile
- scripts/welltrack-lab.py: Welltrack Lab - Interactive Marimo main file

### Tools

- scripts/create-sample-data.py: python script to create example data for welltrack.html to import
- scripts/dev_serve.py: python script for https serving a directory (will generate a selfsigned ssl certificate on the fly)

### Build and Config files

- Makefile: central make file for building and developing
    - `make` or `make help` for usage
    - `buildenv`             Create build environment in $PWD/.venv
    - `clean`                Remove test and build artifacts
    - `clean-all`            Remove environment and all artifacts
    - `docs`                 Make Onlinepage and WebApp
    - `dev-serve`            HTTP Serve Documentation on port 8000
    - `dev-serve-ssl`        HTTPS Serve Documentation on port 8443
    - `lab`                  Edit welltrack-lab.py in marimo
    - `lint`                 Run Linting
    - `test`                 Create Sample Data, run Tests
- mkdocs.yml: mkdocs configuration
    - In mkdocs.yml, file paths in the nav section are relative to the docs directory, not the project root.
- pyproject.toml: python dependencies for interactive marimo, testing and mkdocs build
- build/site/: mkdocs homepage
- build/site/wheel/: welltrack_lab Library as wheel for integration in build/site/marimo
- build/site/marimo/: Welltrack-Lab Interactive Mario html wasm page
- build/site/welltrack/: Welltrack Main SingePage WebApp page

### Main Welltrack Webapp

- The application is a single-page application (SPA) contained entirely within src/welltrack/welltrack.html.
- The application's UI is in German.
- User prefers long dates to be formatted as 'Weekday Day.Month.Year' in German (e.g., 'Montag 29.9.2025').
- The application uses localStorage for all data storage, making it a client-side-only application with no backend.
- Dependencies like Tailwind CSS, Chart.js, and date-fns are loaded via CDNs.
- Use python playwright for GUI Testing.
- Python scripts related to welltrack data creation/parsing, should read configuration of mood types and body parts directly from src/welltrack/welltrack.html using regex to ensure they are in sync with the main application's settings.

#### Implementation Specifics

- A data 'slot' for mood or pain is defined as all entries of that type within a 10-minute window, calculated forwards from the first entry in a given subset

#### Playwright GUI Testing and Verification of Welltrack

- run `make test` creates a sample data file under `build/tests/sample-data.json`, starts the dev_server and runs all integrated playwright tests in `tests/`
- to run the dev server manually, run `source .venv/bin/activate && python scripts/dev_serve.py -d build/site 8443 > dev_server.log 2>&1 &`
- for specific playwright gui testing run `mkdir -p build/tests/output; source .venv/bin/activate pytest --device "Pixel 7" --screenshot on --video retain-on-failure --output build/tests/output` and the testfilename.

- In Playwright, to check if a modal has been hidden (i.e., has the 'hidden' class), use expect(locator).to_be_hidden() instead of wait_for_selector('.hidden'), as the latter will time out waiting for a hidden element to become visible.
- In Playwright, element selectors like page.get_by_title() are case-sensitive and must exactly match the attribute value in the HTML.
- For single-page applications, Playwright scripts should avoid using page.reload() after navigation clicks, as this can reset the application state and cause tests to fail. The expect function's built-in wait is sufficient to handle asynchronous rendering.
- When using Playwright to test features that are not initially visible on the page (e.g., at the bottom of a long scroll), use page.screenshot({ full_page: True }) to capture the entire page content for verification.
- When using Playwright's to_have_class assertion, the argument must be a string or a regular expression, not a lambda function. A regular expression like re.compile(r'\bactive\b') can be used to check for the presence of a class.


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
