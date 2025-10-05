# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- **[x] Data Migration**:
  - Add migration code to automatically rename the old `wellTrackEvents` LocalStorage key to `wellTrackEventTypes`.
  - Update the JSON import logic to recognize and rename the legacy `events` key to `eventTypes`.
  - Enhance the import validation to check for `metrics`, `events` or `eventTypes`, and `settings`.

- **[x] Notifications**:
  - Implement notifications to confirm the number of items imported after merging or overwriting data.
  - Add a "Daten exportiert" (Data exported) notification after a successful export.
  - Add an "Alle Daten gelöscht" (All data deleted) notification after deleting all data.

- **[x] UI & UX Improvements**:
  - In the "Edit Event Types" section, display a more user-friendly message ("Es gibt keine Einträge dieser Art.") when an event type with no associated entries is deleted.
  - On the "About" page, increase the text size and improve the overall layout to be more appealing.

- **[x] Submenu Layout Refactoring**:
  - Refactor the submenus on the `eventEntry`, `MoodEntry`, `PainEntry`, `Verlauf` (History), and `Settings` pages to use a new CSS-based layout strategy. The new layout should feature a left-aligned title and a right-aligned, overflowing submenu.
  - Create six distinct groups within the `eventEntry` page.
  - Capture screenshots of each refactored subpage for verification.

- **Settings: Edit Event Type - "Nur Aufzeichnen"**: In the event type settings, add a new option to the "Anzeige-Art" (Display Type) dropdown called "Nur Aufzeichnen" (Record Only). This option will be the last in the list: "Zusammenzählen, Einzeln Hervorheben, Einzeln, Nur Aufzeichnen". Events set to "Nur Aufzeichnen" will not be included in the daily summary on the "Today" page and will not appear in the history diagrams (`Verlauf`).

- **Protokoll (Log) Enhancements**:
  - **Time-Based Sorting**: Modify the "Protokoll" (Log) page to sort entries within a single day by time, with the newest entries appearing first. The sorting order for entries with the same timestamp should be: push-button events, other timestamped events, mood entries, and then pain entries.
  - **Remove `ENTRIES_PER_PAGE`**: Eliminate the use of the `ENTRIES_PER_PAGE` constant and any associated logic, as the log will now be paginated by week instead of by a fixed number of entries.

- **Version Update Notification**: Implement a system to notify the user of application updates.
  - On application load or refresh, check the last modified timestamp of the `welltrack.html` file.
  - If this timestamp is more recent than the one stored in `settings:welltrack_latest`, display a brief overlay notification (e.g., "Aktualisiert auf die Version 23.4.2025 23:25") and update the `settings:welltrack_latest` value.
  - The current version timestamp should also be displayed in the "About" section of the settings.

- **Settings: Event Type Editor Modal**: Convert the event type editor into a modal overlay.
  - The modal should fit the viewport horizontally with slim padding and margins to maximize content width, consistent with the visual style of other modals in the application.
  - A click outside the modal or on the "Abbrechen" (Cancel) button should close the modal without saving changes.

- **Refactor: Event Type Naming**:
  - Rename the `getEvents()` function, the `wellTrackEvents` localStorage key, and all related variables to reflect that they handle an array of event *types*, not event instances. The new naming convention should be `getEventTypes`, `wellTrackEventTypes`, etc.

- **Refactor: `localStorage` Consolidation**:
  - Refactor the code to use only three main items in `localStorage`: `wellTrackSettings`, `wellTrackEventTypes`, and `wellTrackMetrics`.
  - Migrate any other data currently stored directly in `localStorage` (e.g., UI state) into the `wellTrackSettings` object.
  - Ensure that the application state is correctly initialized from the `wellTrackSettings` object on page load and that any changes are saved back to it.

## Discovered Tasks