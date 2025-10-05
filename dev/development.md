# Project Development Documentation

## Files and Directories Layout

### Development Documents

- dev/system-workflow.md: Development process and coding conventions.
- dev/product-requirements.md: High-level functional and non-functional requirements.
- dev/development.md: (This file) The project file layout, architectural overview and developer guidlines for working with project.
- dev/product-specifications.md: Low-Level functional and non-functional specifications.
- dev/tasks.md: A living document tracking already completed and new to be done tasks.

### User Documentation

- README.md: A user centric view on howto use the app. It is the primary source of user documentation and should be kept in sync with new features, including adding new sections and placeholders for screenshots.
- assets/*.png: The screenshots mainly used for README.md
- docs: a mostly symlinked directory (including ../README.md and ../assests, and ../src/welltrack/icon*) for mkdocs

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
    - `buildenv`             Create build environment
    - `clean`                Remove test and build artifacts
    - `clean-all`            Remove environment and all artifacts
    - `docs`                 Make Onlinepage and WebApp
    - `docs-serve `          HTTP Serve Documentation on port 8000
    - `docs-serve-ssl`       HTTPS Serve Documentation on port 8443
    - `lab`                  Edit welltrack-lab.py in marimo
    - `lint`                 Run Linting
    - `test`                 Run Tests
- mkdocs.yml: mkdocs configuration
- pyproject.toml: python dependencies for interactive marimo, testing and mkdocs build

### Documentation, Language and User Interface

The application's UI is in German. The README.md is in German.

User prefers long dates to be formatted as 'Weekday Day.Month.Year' in German (e.g., 'Montag 29.9.2025').

Avoid using formal personal pronouns like 'Sie' or 'Du' in the documentation, preferring a neutral tone.

### Main Welltrack Webapp

The application is a single-page application (SPA) contained entirely within src/welltrack/welltrack.html.

The application uses localStorage for all data storage, making it a client-side-only application with no backend.

Dependencies like Tailwind CSS, Chart.js, and date-fns are loaded via CDNs.

#### Architecture

A data 'slot' for mood or pain is defined as all entries of that type within a 10-minute window, calculated backwards from the most recent entry in a given set.


## Python Style & Conventions

- **Use uv** (the virtual environment and package manager) whenever executing Python commands, including for unit tests.
- At the start of a new session
    - recreate python environment with "uv venv"
    - install packages with "uv pip install . -e"
- **Use `pyproject.toml`** to write down new used dependencies.
- **Use python_dotenv and load_env()** for environment variables.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
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
