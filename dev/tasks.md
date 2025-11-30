# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

- [x] **Prototype: New Pain Entry**: Create a prototype in `src/prototype/new-pain-entry.html` with new pain entry logic, split body parts, and custom pain types.
    - [x] Create skeleton and basic views (Home, Pain, Settings).
    - [x] Refactor SVGs (Split LWS/KSB, Split Chest/Abdomen).
    - [x] Implement Pain Entry logic (10 min reset/replace).
    - [x] Implement "Weitere" tab with Pain Free item and custom items.
    - [x] Implement Settings tab for custom pain types.
    - [x] Implement Drag and Drop reordering for pain types.
    - [x] Create verification tests and screenshots.

## Completed Tasks

- [x] **Refactor Submenu Layouts**: Update the submenu layout on the Event, Mood, Pain, History, and Settings tabs. The title will be on its own line, and the submenu will be on the next line, right-aligned, with items flowing from right to left and wrapping downwards.
- [x] **Refactor Log Page Layout**: Adjust the log/protocol page so the title and protocol selector form a fixed unit attached to the header bar, preventing them from moving with the content.
- [x] **Refactor PushButton Event Layout**: In the Event Entry tab, modify the "PushButton" layout to ensure the title (e.g., "Titel [(4x, zuletzt um hh:mm)]") is on one line and the action buttons ("Einnahme", "Rückgängig", "Erneute Einnahme") are on a second, right-aligned line. This will create a stable UI that does not change size based on the button state.
- [x] **Fix GUI Flicker**: Resolve the layout flicker on event entry pushbuttons.
- [x] **Restyle Pushbutton Event Info**: Align the timestamp text to the right, remove parentheses, and make it semibold.

## Discovered Tasks
