# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks


- [X] **Create Prototype Skeleton**: Create `src/prototype/new-pain-entry.html` with a skeleton WellTrack GUI mainbar and Tailwind CSS. Expose only the body pain interface. Implement a "Home" icon to reveal current metrics. Refactor out body SVGs and selection logic.
- [X] **Refactor SVGs**:
    - Split "LWS" vertically (Upper: LWS, Lower: KSB "Kreuz & Steißbein").
    - Split "Brust" and "Bauch" into left and right parts.
    - Remove "pain_free" elements from SVGs.
- [X] **Implement "Weitere" Subselector**:
    - Create a new "Weitere" section with a two-column list.
    - Add "Schmerzfrei" as the first item using the icon from `src/prototype/pain-free-selector.html`.
    - Add custom pain entries (e.g., "Tinitus", "Sodbrennen").
- [X] **Implement Pain Entry Logic**:
    - **Initialization**: Color body parts based on metrics from the last 10 minutes.
    - **Entry**: Replace existing entries of the same type within the last 10 minutes.
    - **10-Minute Window**: Allow changing/deleting entries within 10 minutes.
    - **Pain Free**: Implement "Wieder Schmerzfrei?" modal and history cleanup logic.
- [X] **Create Settings Submenu**: Create a "Schmerzarten" submenu to manage custom pain entries.
- [X] **Verify Prototype**: Create a test `tests/test_new_pain_entry.py` to open the prototype and take screenshots (Back, Front, Other). Verify screenshots.

## Discovered Tasks
