# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

- **`extract_mood_pain.py` script:**
  - Create a Python script to extract mood and pain entries from a WellTrack JSON export.
  - The script will accept a start date (`dd.mm.yyyy` or `all`) as a command-line argument.
  - It will read data from `stdin`, filter entries, and validate them against the current `welltrack.html` configuration.
  - Invalid entries will be reported to `stderr`, and the filtered, valid JSON will be printed to `stdout`.

This update includes a comprehensive set of UI enhancements, feature additions, and behavioral refinements across the application.

- **UI & Styling:**
  - Redesigned "Today" tab pills for mood, pain, and events to improve readability and handle long text. The "gleichbleibend" trend indicator now correctly uses a right-arrow icon and an equals sign. Event pills now default to a horizontal layout and wrap vertically when needed.
  - Cleaned up the "Event Entry" tab by reorganizing buttons to appear on the same line as the event name when space permits.
  - Standardized all tab and section heading sizes for a consistent look and feel.
  - Reverted the subgroup selectors on the "Event Entry" and "Verlauf" tabs to their original "connected" style.

- **Features & Logic:**
  - Updated the data aggregation for mood and pain charts to group data into 10-minute timeslots, allowing for intra-day visualization.
  - Implemented a "Pain-Free" button on the pain entry screen to allow users to log periods of no pain.
  - Refined the mood slider to prevent accidental selections when scrolling.
  - Updated the "delete event type" logic to count existing entries, display a detailed confirmation message, and delete both the event type and its associated data.
  - Refactored the `is_cumulative` field into a new `displayType` setting with three options ("Zusammenzählen," "Einzeln, hervorheben," "Einzeln") to control how events are grouped and displayed.
  - Enhanced the data import/merge functionality to prevent overwriting existing event configurations and to reconstruct metric labels based on current app settings.

## Discovered Tasks