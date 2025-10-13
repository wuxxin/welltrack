# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- [x] **Create Dark Theme Tests**:
    - Create a test suite in `tests/test_darktheme.py` to capture screenshots of all main tabs in both light and dark modes for visual verification. The screenshots should be saved in `build/tests/darktheme/`.
- [x] **Implement Dark Theme**:
    - Add a dark theme to the application.
    - Add a theme switcher in Settings > Darstellung with options: "Automatisch", "Hell", "Dunkel". Default to "Automatisch".
    - "Automatisch" should respect the user's browser/OS preference.
    - Before implementing, refactor and clean up existing CSS.
    - Ensure high contrast and appropriate color adjustments for all components in dark mode.
- [x] **Fix GUI Flicker**: On an event entry pushbutton, the layout flickers when toggling between selected and unselected states. The container size must be stabilized to prevent this.
- [x] **Refactor Submenu Layouts**: Update the submenu layout on the Event, Mood, Pain, History, and Settings tabs. The title will be on its own line, and the submenu will be on the next line, right-aligned, with items flowing from right to left and wrapping downwards.
- [x] **Refactor Log Page Layout**: Adjust the log/protocol page so the title and protocol selector form a fixed unit attached to the header bar, preventing them from moving with the content.
- [x] **Refactor PushButton Event Layout**: In the Event Entry tab, modify the "PushButton" layout to ensure the title (e.g., "Titel [(4x, zuletzt um hh:mm)]") is on one line and the action buttons ("Einnahme", "Rückgängig", "Erneute Einnahme") are on a second, right-aligned line. This will create a stable UI that does not change size based on the button state.

## Discovered Tasks