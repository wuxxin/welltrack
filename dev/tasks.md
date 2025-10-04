# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

- **2025-10-04 (Refactoring & Feature Update)**:
    - **Refactor Naming:** Rename `getEvents` to `getEventTypes`, `wellTrackEvents` to `wellTrackEventTypes`, and related variables to improve clarity.
    - **Refactor LocalStorage:** Consolidate `wellTrackPainView`, `wellTrackLogVisibility`, and `wellTrackActiveSettingsTab` into the main `wellTrackSettings` object.
    - **Sortable Event Types:** Implement a "Reihenfolge verändern" (Change Order) mode in the settings to allow users to reorder event types via drag-and-drop.
    - **New Display Type:** Add a "Nur Aufzeichnen" (Record Only) display type for events, which will not appear on the Today page or in history charts.
    - **Log Sorting:** Sort log entries on the "Protokoll" and "Today" pages by newest first and remove the unused `ENTRIES_PER_PAGE` config.

- **2025-10-03 (Final Polish)**: Final UI Polish
    - **Card Styling:** Reduce padding and border-radius on all cards for a tighter layout.

## Completed Tasks

- **2025-10-03 (Follow-up)**: UI Refinements and Layout Adjustments
    - [x] **Spacing & Alignment:** Reduced top-level spacing and ensured consistent title alignment across all pages.
    - [x] **Log Page Header:** Placed title and week selector on a single responsive line.
    - [x] **Sub-Tabs:** Decreased spacing between sub-tab buttons for a more cohesive look.
    - [x] **History Page Charts:** Removed card container to make charts span the full viewport width.

- **2025-10-03**: Full-stack UI Refactoring and Feature Implementation
    - [x] **Modals & Settings UI:** Improved modal dialogs (delete event, data import) for better viewport fit and readability. Auto-scrolled to the edit form.
    - [x] **Today Page:** Redesigned Mood/Pain pills for better visual prominence of data.
    - [x] **Tab/Sub-Tab Layout:** Refactored all sub-tab selectors for consistent, mobile-first, and appealing overflow behavior.
    - [x] **History Page:** Moved charts to a full-width container for better visibility.
    - [x] **Log Page:** Implemented a new week-based, sticky pagination system and updated the log display accordingly.

## Discovered Tasks
