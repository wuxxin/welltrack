# **Project Layout & Architecture for WellTrack**

## Development Documents

Files:

* dev/system-workflow.md: Development process and coding conventions.
* dev/product-requirements.md: High-level functional and non-functional requirements.
* dev/project-structure.md: (This file) The file and architectural overview.
* dev/tasks.md: A living document tracking already completed and new to be done tasks.

## User Documentation

Files:

* README.md: A user centric view on howto use the app. It is the primary source of user documentation and should be kept in sync with new features, including adding new sections and placeholders for screenshots.
* assets/*.png: The screenshots mainly used for README.md
* docs: a mostly symlinked directory (including ../README.md and ../assests, and ../src/welltrack/icon*) for mkdocs

## Software

### Main Welltrack Webapp Software and Assets

Files:

* src/welltrack:
    * welltrack.html: The main application file containing all HTML, CSS, and JavaScript
    * sw.js: The service worker for PWA caching and offline capabilities like notifications
    * manifest.json: The PWA web app manifest
    * icon-192.png: Application icons
    * icon-512.png: Application icons


The application is a single-page application (SPA) contained entirely within src/welltrack/welltrack.html.

The application uses localStorage for all data storage, making it a client-side-only application with no backend.

Dependencies like Tailwind CSS, Chart.js, and date-fns are loaded via CDNs.


### Documentation, Language and User Interface

The application's UI is in German. The README.md is in German.

User prefers long dates to be formatted as 'Weekday Day.Month.Year' in German (e.g., 'Montag 29.9.2025').

* avoid using formal personal pronouns like 'Sie' or 'Du' in the documentation, preferring a neutral tone.

### Architecture

A data 'slot' for mood or pain is defined as all entries of that type within a 10-minute window, calculated backwards from the most recent entry in a given set.


### Welltrack-Lab - Interactive Marimo Python Webapp

Files:

* src/welltrack_lab/: Welltrack Lab - Python Library and Tools
* scripts/welltrack-lab.py: Welltrack Lab - Interactive Marimo main file

### Example Data Creation for import in Welltrack - Python script

Files:

* scripts/create-sample-data.py: python script to create example data for welltrack.html to import

### build and config files

* Makefile:
* mkdocs.yml: mkdocs configuration
* pyproject.toml: dependencies for interactive marimo, testing and mkdocs build


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

