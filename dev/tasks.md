# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- [x] **GUI Dark Theme**:
    - Implement a dark theme for the application.
    - Add a theme switcher in the settings under "Darstellung" > "Design" with options: "Automatisch", "Hell", "Dunkel". Default to "Automatisch".
    - "Automatisch" should use the browser's preferred color scheme, defaulting to light mode if not available.
    - Refactor and clean up existing CSS during implementation.
    - Ensure good contrast and readability in dark mode, with dark backgrounds and light foregrounds.
    - Create a new test suite `tests/test_darktheme.py` to capture screenshots of all main tabs in both light and dark modes for visual verification. The screenshots should be saved to `build/tests/darktheme/`.
- [x] **Refactor Submenu Layouts**: Update the submenu layout on the Event, Mood, Pain, History, and Settings tabs. The title will be on its own line, and the submenu will be on the next line, right-aligned, with items flowing from right to left and wrapping downwards.
- [x] **Refactor Log Page Layout**: Adjust the log/protocol page so the title and protocol selector form a fixed unit attached to the header bar, preventing them from moving with the content.
- [x] **Refactor PushButton Event Layout**: In the Event Entry tab, modify the "PushButton" layout to ensure the title (e.g., "Titel [(4x, zuletzt um hh:mm)]") is on one line and the action buttons ("Einnahme", "Rückgängig", "Erneute Einnahme") are on a second, right-aligned line. This will create a stable UI that does not change size based on the button state.
- [x] **Fix GUI Flicker**: Resolve the layout flicker on event entry pushbuttons.
- [x] **Restyle Pushbutton Event Info**: Align the timestamp text to the right, remove parentheses, and make it semibold.

## Discovered Tasks
