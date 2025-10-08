# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

- **Rebirth Message & `console.log` Refactor**: Refactor all `console.log()` calls adjacent to `location.reload()` to use a new "rebirth message" system. This involves saving a message to `localStorage` before the reload. Upon re-initialization, the application will check for this message and display it in an overlay. This overlay will be styled similarly to the version update modal but can be displayed concurrently. The layout will be linear: `icon Title-in-Bold Message`. A new setting, `hide_modal_overlays`, will be added to `localStorage` to disable these overlays for clean testing screenshots.

- **"Heute = 05-05" Feature**: Implement a "WellTrack day" that runs from 5:00 AM to 4:59 AM the next day. This affects the "Heute" page, which will display "Heute -> Montag auf Dienstag..." between midnight and 5:00 AM. Daily values for push-button events will reset at 5:00 AM, and entries made before this time will count towards the previous day. This change will also affect event entry and undo logic. The start time for a new day will be configurable in the settings.

- **Protokoll Refactor**: Overhaul the "Protokoll" (log) view. The layout will be updated to feature a sticky week selector and a fixed, left-aligned date display that clarifies the "5-to-5" day (e.g., "Dienstag 7.10.2025 auf Mittwoch"). Timestamps will use icons to differentiate between same-day and next-day (pre-5:00 AM) entries. The data gathering logic will be rewritten to align with the new day definition. Mood and pain entries will be grouped into 10-minute slots, reversed, and sorted alphabetically. "Ereignisse" will be reordered, and entries without a group will be labeled "Allgemein".

## Completed Tasks

- **GUI Test Implementation**: Create a suite of GUI tests using pytest-playwright. The tests should cover the initial application states (no data, empty data, sample data) and basic navigation. The test runner should be integrated into the `Makefile` under the `test` target. All tests will run in a 1080x1920 portrait mode, and screenshots of failed tests will be saved.

## Discovered Tasks