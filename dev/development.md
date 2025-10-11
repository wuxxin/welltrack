# WellTrack Developer Documentation

This document provides a comprehensive guide for developers working on the WellTrack project. It covers the project's purpose, architecture, setup, and conventions.

## 1. Project Purpose and Philosophy

WellTrack is a 100% private, client-side health diary designed for easy and fast logging of personal health metrics like mood, pain, and daily events. Its core philosophies are:

- **Privacy First:** All data is stored exclusively in the browser's `localStorage`. There is no backend server, and no data ever leaves the user's device unless explicitly exported by them.
- **Offline Capability:** As a Progressive Web App (PWA), WellTrack is fully functional without an internet connection after the initial load.
- **Simplicity and Speed:** The UI is designed for rapid data entry, minimizing clicks and friction.
- **Zero-Build Frontend:** The main application is a single HTML file that requires no build step. Dependencies are loaded via CDNs, allowing for simple "drag-and-drop" updates.

## 2. Project Architecture

The project consists of two main parts: the **WellTrack Webapp** and the **WellTrack Lab**.

### 2.1. WellTrack Webapp

This is the core single-page application (SPA) that users interact with.

- **File:** `src/welltrack/welltrack.html`
- **Technology:** Vanilla JavaScript, HTML5, Tailwind CSS. All code is contained within the single HTML file.
- **Data Storage:** `localStorage` is used for all data, including metrics, event type definitions, and user settings.
- **Structure:** The JavaScript code is organized within a single global object, `WellTrackApp`, which is further divided into namespaces for state management (`state`), configuration (`config`), data handling (`data`), UI rendering (`render`), event handling (`events`), and utilities (`utils`).

### 2.2. WellTrack Lab

This is an interactive data analysis tool built with Marimo.

- **File:** `scripts/welltrack-lab.py`
- **Technology:** Python, Marimo, Pandas.
- **Purpose:** Allows users to upload their exported `welltrack.json` file and perform more advanced data analysis and visualization in an interactive notebook environment.

### 2.3. Directory Layout

```
/
├── assets/                 # User-facing images and screenshots for documentation
├── build/                  # Build artifacts (not version controlled)
│   ├── site/               # Generated mkdocs site
│   └── tests/              # Test-related outputs (e.g., screenshots, sample data)
├── dev/                    # Development and project documentation
├── docs/                   # Source files for user documentation (mkdocs)
├── scripts/                # Helper scripts for development
├── src/                    # Source code
│   ├── welltrack/          # Core web application files
│   └── welltrack_lab/      # Python library for the Marimo lab
└── tests/                  # Automated tests (Playwright)
```

## 3. Setup and Development Workflow

### 3.1. Initial Setup

1.  **Clone the repository.**
2.  **Create the virtual environment and install dependencies:**
    ```bash
    make buildenv
    ```
    This command uses `uv` to create a `.venv` and install all necessary Python packages from `pyproject.toml`. It also installs the required Playwright browser dependencies.

### 3.2. Common Tasks

-   **Run the development server:** To serve the application locally over HTTPS (required for PWA features), run:
    ```bash
    make dev-serve-ssl
    ```
    The application will be available at `https://localhost:8443/welltrack/welltrack.html`. The server uses a self-signed certificate, so you will need to accept the browser's security warning.

-   **Generate the full build:** To build the user documentation and copy all application files into the `build/site` directory (which the dev server serves), run:
    ```bash
    make docs
    ```

-   **Run tests:** To run the complete test suite (which includes creating sample data and running Playwright tests), use:
    ```bash
    make test
    ```

-   **Run the WellTrack Lab:** To start the Marimo editor for the lab notebook, run:
    ```bash
    make lab
    ```

## 4. Data Architecture

All application data is stored in the browser's `localStorage` under three main keys:

1.  `wellTrackMetrics`: An array of metric objects.
2.  `wellTrackEventTypes`: An array of objects defining custom event types.
3.  `wellTrackSettings`: A key-value object for user preferences.

### 4.1. The Metric Entry Format

The data format is inspired by Prometheus, where each entry is a timestamped measurement.

```json
{
  "metric": "metric_name_suffix",
  "timestamp": 1672531200000, // Unix timestamp in milliseconds
  "value": 123,
  "labels": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

### 4.2. Metric Types

There are three main categories of metrics:

#### a) Time-based Value Entries (Cumulative Events)

-   **Purpose:** To track activities where the total amount per day is what matters (e.g., minutes walked, pages read).
-   **Example:** A user logs "15 min" for a walk. Later, they log another "30 min". The application stores a single entry for that day with `value: 45`.
-   **Implementation:** These events have `displayType: 0` and a non-zero `increment`. The `addMetric` function finds an existing entry for the same activity on the current "WellTrack Day" and updates its value.

#### b) Push Button Events (Timestamp Events)

-   **Purpose:** To log the occurrence of an event at a specific time (e.g., taking medication, having a coffee).
-   **Example:** A user clicks the "Ibuprofen" button. An entry is created with the current timestamp.
-   **Implementation:** These events have `displayType: 2` and `increment: 0`. A new metric entry is created for each click. The UI then counts the number of entries for the day to display the total.

#### c) Mood and Pain Entries (10-Minute Timeslots)

-   **Purpose:** To allow users to fine-tune their mood or pain entries without creating excessive data points.
-   **Example:** A user logs their mood. Five minutes later, they realize a rating was wrong and change it. The application updates the original entry instead of creating a new one.
-   **Implementation:** When a mood or pain metric is logged, the `addMetric` function checks if another entry for the *exact same item* (e.g., the same mood question or body part) exists within the last 10 minutes. If so, it replaces the old entry with the new one. This moving 10-minute window is what defines a "timeslot" for these entries.

### 4.3. Data Export Format

The export function bundles all three `localStorage` items into a single JSON file, making backup and migration straightforward.

```json
{
  "metrics": [...],
  "eventTypes": [...],
  "settings": {...}
}
```

## 5. GUI Tabs Overview

The application is structured into several tabs, accessible from the main navigation header.

-   **Heute (Today):** The main dashboard. It shows summary cards for the latest mood and pain scores with a comparison to the previous entry. It also displays cards for event groups that have activity today. A collapsible section at the bottom shows a detailed, time-stamped log of all entries for the current WellTrack day.
-   **Ereignis (Event):** The primary page for logging events. Events are grouped by type, and users can interact with buttons to log timestamp events or increment/decrement cumulative events.
-   **Stimmung (Mood):** The mood logging page. Moods are organized into groups (e.g., "Energy & Motivation"). Users rate various aspects on a -3 to +3 scale using sliders.
-   **Schmerz (Pain):** The pain logging page. Users select body parts on an interactive SVG diagram (front and back views) and rate the pain intensity on a 0-5 scale in a modal dialog.
-   **Verlauf (History):** The visualization page. It contains charts for Events, Mood, and Pain, which can be filtered by time ranges (7, 28, or 84 days).
-   **Protokoll (Log):** A paginated, chronological list of all recorded data, grouped by day. It provides a detailed breakdown of all entries.
-   **Einstellungen (Settings):** The settings page, which is further divided into sub-tabs for managing event types, importing/exporting data, configuring notifications, and setting display options like the start time of the day.

## 6. Code Style and Conventions

-   **JavaScript:** The code is written in vanilla ES6+. It is self-contained within the `welltrack.html` file and does not use a transpiler or bundler. JSDoc is used for documentation.
-   **Python:** Scripts follow PEP8 standards and use Google-style docstrings. `black` is used for formatting.
-   **Dependencies:** The project uses `uv` for Python package management. Frontend dependencies are loaded from CDNs.