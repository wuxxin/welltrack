# Changelog

This document lists the implementation status of features and refactorings for the WellTrack health diary app.

## Implemented Features

**2025-09-23: Major Refactoring of Data Logic and UI**
- Switched all internal timestamps from ISO strings to epoch seconds for more efficient processing.
- Reworked data entry logic for all metric types (Events, Mood, Pain).
- **Events:** Incrementing events on the same day now update a single entry instead of creating new ones.
- **Mood & Pain:** Entries are now updated if made within a 10-minute window, otherwise a new, separate entry is created. UI fields are automatically cleared after this 10-minute window.
- Updated UI components:
- Removed "+1" buttons for mood/pain, as the new logic makes them obsolete.
- The pain tracking page now has a static title "Schmerzen".
- The time of the last entry is now displayed next to the "Stimmung" and "Schmerzen" titles.
- The detailed log view ("Protokoll") now groups multiple timestamp-based events for a cleaner summary.
- Rebuilt the pain history chart to be a stacked bar chart (for individual pain points) with a cumulative line graph and moving average, similar to the mood chart.
- Standardized all user-facing dates and times to German format (dd.mm.yyyy, HH:MM).
- Corrected the CDN link for the `date-fns` library.
- Change all epoch seconds to standard epoch milliseconds in `welltrack.html` for consistency.
- Repair `create_sampledata.py` to ensure all body parts, moods, and standard event types are sourced directly from `welltrack.html`.
- Update `create_sampledata.py` to generate timestamps in milliseconds.


**2025-09-24: UI/UX Improvements and Refactoring**
- **Mood Entry:** Prevented mood ruler clicks during page scroll by distinguishing between click and drag events.
- **Today Page:**
    - Redesigned header to split "Heute" and the date for better readability.
    - Redesigned summary cards to be more compact, space-efficient, and visually informative.
- **Event Entry:** Improved layout of event items to fit on a single line, even on smaller screens.
- **History Charts:**
    - Set a height of 600px for all charts.
    - Reverted dynamic width scaling for charts, maintaining a consistent 100% width.
- **Log Page (Protokoll):**
    - Made log cards wider with a larger base font size for better readability.
    - Restructured the card layout with the date positioned in the top-right, in the normal content flow.
    - Implemented a structured matrix/grid display (3-4 columns) for Mood and Pain sub-metrics.
    - Applied consistent color-coding to all relevant values.
    - Hid timestamps for incrementing (non-timestamp) events.
    - Re-formatted timestamp events to "Um hh:mm: [Event Name]".


**2025-09-25: Comprehensive Refactoring and UI/UX Enhancements**
- **Refactored Data Entry Logic:**
  - Removed the `committedIndex` system entirely, simplifying data management.
  - Implemented a new `addMetric` helper function to handle all data entries.
  - **De-duplication Logic:**
    - Event entries with increments now update the existing value if logged on the same day.
    - Mood and Pain entries now update the previous value if made within a 10-minute window, preventing duplicate entries for the same feeling.
- **Improved "Verlauf" (History) Page Calculations:**
  - The moving average (mvg) calculation is now time-weighted for Mood and Pain, reflecting the duration each value was active for a more accurate trend analysis.
  - For days with no pain data, a value of 0 is now assumed at noon to ensure a continuous moving average line.
  - All moving average values are now rounded to two decimal places.
- **Redesigned "Today" Page:**
  - The page now prioritizes Mood and Pain summary cards.
  - Below these, new cards for each event group are displayed. These cards are clickable and navigate directly to the "Events" page with the corresponding group tab pre-selected.
- **UI Enhancements:**
  - **Events Page:** The `+` and `-` buttons for incrementing events were replaced with centered Material Symbols icons for better visual alignment and consistency.
- **Security Hardening:**
  - Implemented a strict Content Security Policy (CSP) via a `<meta>` tag to restrict resource loading to trusted CDNs and prevent potential cross-site scripting (XSS) attacks.


**2025-09-28: Settings, Grouping Logic, and UI Refactoring**
- **Settings Refactor:**
  - Removed the "days" selection for event types entirely from the UI and data model.
  - Added a new boolean checkbox `is_cumulative` to the event editor, allowing users to define whether events of the same type should be aggregated. This is enabled by default.
  - The underlying data handling for events was updated to support this new property, and a migration path ensures older data is handled gracefully.
- **"Today" and "Verlauf" Page Refactoring:**
  - Rebuilt the display logic for events on both the "Today" dashboard and the "Verlauf" (History) charts.
  - Events are now grouped based on a new set of rules: events are aggregated if they share the same `groupType`, the same `unitType` (which must be a meaningful string), and have the `is_cumulative` flag set to `true`.
  - On the "Today" page, this results in single, cumulative cards for aggregated groups.
  - In the "Verlauf" charts, this creates a single, consolidated line chart for each aggregated group, with the Y-axis correctly labeled (e.g., "Bewegung (min)").
  - All non-cumulative events are displayed individually as before, maintaining clarity.
- **GUI Refactoring:**
  - The event cards on the "Today" page are now arranged in a responsive "automatrix" grid that automatically adjusts between 2 and 3 columns based on screen width, falling back to a single column on very small screens.
  - The "Protokoll" (Log) page's mood and pain detail views were updated to use a more compact and consistent grid, displaying between 2 and 4 columns for better readability.


**2025-09-28: Bug Fixes and Configuration Update**
- **Bug Fix:** The "edit" button in the event type settings was non-functional. This was resolved by correcting the `onclick` handler to pass the event's index instead of the entire object, allowing the edit form to populate correctly.
- **Config Update:** The default event "Kaffee Tassen" is now set to be non-cumulative (`is_cumulative: false`) for new users.


**2025-09-29: Final Bug Fixes and Configuration**
- **Bug Fix:** The "edit event" functionality was definitively repaired by refactoring the `handleSaveEvent` function. The logic now correctly uses the `activity` ID from the application's state when editing, ensuring the correct event is always updated.
- **Config Update:** The default `unitType` for the "Ibuprofen 400mg" event was changed from "Einnahme" to an empty string (`""`) for better clarity in the UI.


**2025-09-29: Final Polish and CSP Fix**
- **Bug Fix:** A JavaScript `TypeError` that occurred when opening the event editor was resolved by removing obsolete code related to the old "days" selection feature.
- **CSP Fix:** The Content Security Policy was corrected by removing the `frame-ancestors` directive (which is not supported in meta tags) and adding `https://cdn.jsdelivr.net` to `connect-src` to allow Chart.js to fetch its source maps, resolving console errors.


**2025-09-29: Feature Update and UI/UX Overhaul**
- **Documentation (`README.md`):**
  - Add clear links to the live GitHub Pages application.
  - Add a new section explaining how to "install" the PWA on a smartphone, including the provided screenshot.
  - Clarify the difference between using the live page and a local file regarding updates.
- **GUI and Styling:**
  - **Today Tab:** Re-style the event and mood cards into a more organized matrix layout.
  - **Mood Tab:** Change mood entry to trigger on click release (mouseup) and prevent firing on scroll.
  - **General Style:**
    - Make all cards full-width.
    - Ensure consistent padding on mood cards.
    - Add a hover color to all clickable buttons.
- **"PushButton" Event Logic:**
  - The first button will be named after the event's `unitType`.
  - After a click, it will be replaced by "Rückgängig" (Undo) and "Erneut/e [unitType]" (Again) buttons.
  - "Erneut" will log a new event immediately.
  - "Rückgängig" will undo the last entry of the day; if it's the last one, the UI reverts to the initial state.
- **Reminder Settings:**
  - **Inactive State:** Show "Status: Nicht aktiviert" and an "Aktivieren" button.
  - **Active State:** Show "Status: aktiviert", a text field for multiple reminder times (e.g., "12:00, 17:00"), and "Deaktivieren" and "Test-Benachrichtigung" buttons.
- **Body Pain Feature:**
  - Replace the current body SVGs with the new versions from `new-body-front.html` and `new-body-back.html`.
  - Add German `data-name` attributes to the new SVGs.
  - Update the pain selection modal to display the figure name (e.g., "Rückseite") and the body part name.
  - Add keyboard shortcuts (-, L, U, S, F, X, Escape) to the pain modal.
- **Data Import:**
  - Add a confirmation dialog before import.
  - Provide three options: "Abbrechen" (Cancel), "An bestehende Daten anhängen" (Append), and "Alles überschreiben" (Overwrite).
  - Implement the "Append" logic to merge new event types and chronologically insert new metrics without creating duplicates.


**2025-10-01: UI/UX Enhancements, Logic Refinements, and Documentation**
- **Settings UI:**
  - **Import Logic:** Ensure that merging data via import does not duplicate identical metrics.
  - **Button Colors:**
    - The confirmation button in deletion modals ("Bestätigen") will use the primary error color for high visibility.
    - In the "edit event" modal, the "Speichern" (Save) button will match the color of the "Neue hinzufügen" (Add New) button.
    - In the data import modal, the "Daten vereinen" (Merge Data) and "Daten überschreiben" (Overwrite Data) buttons will be styled as warning/error buttons.
- **"Today" Page UI:**
  - **Card Click Behavior:**
    - The main mood and pain summary cards will be split into two clickable zones: the left side (label) will navigate to the data entry page, while the right side (value/trend) will navigate to the corresponding history chart.
    - Event cards will also be split: the left side (name) will go to the event entry page, and the right side (value) will navigate to the history page and scroll to that event's specific chart.
- **Event Entry UI:**
  - The initial button for "pushbutton" (timestamp) events (e.g., "+ Einnahme") will be styled to match the subsequent "Erneute Einnahme" (Log Again) button for color consistency.
- **Pain Entry UI:**
  - Tooltips will be added to the body part SVGs, revealing the full name of the body part on hover.
- **Documentation:**
  - **`README.md`:**
    - Add a new section describing the optional reminder settings feature.
    - Add a section explaining the functionality of "pushbutton" events.
    - Include a placeholder for a new screenshot demonstrating the pushbutton event flow.
  - **`tasks.md`:**
    - Update the "Planned Tasks" section with a detailed breakdown of the current work.


**2025-10-03: comprehensive set of UI enhancements, feature additions, and behavioral refinements**
- **Today Page Enhancements:**
  - The "Letzte Einträge" section will be converted into a styled button that dynamically displays the number of entries for the day (e.g., "23 heutige Einträge").
  - An expand/collapse icon will be added to the button, which will toggle to indicate the current state.
  - If no entries exist for the day, the button will display "Noch keine Eiträge für Heute" with consistent styling but without an icon.
  - The section's content will be hidden by default, and its visibility state will be persisted in `localStorage`.
  - The pain trend indicator will be updated to show a red up-arrow for increased pain and a green down-arrow for decreased pain.
- **Settings Page Redesign:**
  - The sub-tabs ("Ereignisarten", "Datenverwaltung", "Erinnerungen", "Über") will be restyled to match the appearance of the button group selectors found on the "Verlauf" page.
- **Protokoll Page UX Improvement:**
  - The "Zurück" and "Weiter" pagination buttons will now scroll the viewport to the end of the newly loaded page content, ensuring the buttons remain in a consistent screen position.
- **General UI Alignments:**
  - The sub-tab selectors on the "Stimmung" and "Schmerzen" pages will be aligned to the right on the same line as the page title.
  - The sub-tab selector on the "Verlauf" page will be adjusted to wrap and align to the bottom-right on smaller screens.
- **`extract_mood_pain.py` script:**
  - Create a Python script to extract mood and pain entries from a WellTrack JSON export.
  - The script will accept a start date (`dd.mm.yyyy` or `all`) as a command-line argument.
  - It will read data from `stdin`, filter entries, and validate them against the current `welltrack.html` configuration.
  - Invalid entries will be reported to `stderr`, and the filtered, valid JSON will be printed to `stdout`.
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


**2025-10-03 (Follow-up)**: UI Refinements and Layout Adjustments
- **Spacing & Alignment:** Reduced top-level spacing and ensured consistent title alignment across all pages.
- **Log Page Header:** Placed title and week selector on a single responsive line.
- **Sub-Tabs:** Decreased spacing between sub-tab buttons for a more cohesive look.
- **History Page Charts:** Removed card container to make charts span the full viewport width.

- **2025-10-03**: Full-stack UI Refactoring and Feature Implementation
- **Modals & Settings UI:** Improved modal dialogs (delete event, data import) for better viewport fit and readability. Auto-scrolled to the edit form.
- **Today Page:** Redesigned Mood/Pain pills for better visual prominence of data.
- **Tab/Sub-Tab Layout:** Refactored all sub-tab selectors for consistent, mobile-first, and appealing overflow behavior.
- **History Page:** Moved charts to a full-width container for better visibility.
- **Log Page:** Implemented a new week-based, sticky pagination system and updated the log display accordingly.


**2025-10-03 (Follow-up)**: UI Refinements and Layout Adjustments
- **Spacing & Alignment:** Reduced top-level spacing and ensured consistent title alignment across all pages.
- **Log Page Header:** Placed title and week selector on a single responsive line.
- **Sub-Tabs:** Decreased spacing between sub-tab buttons for a more cohesive look.
- **History Page Charts:** Removed card container to make charts span the full viewport width.

**2025-10-03**: Full-stack UI Refactoring and Feature Implementation
- **Modals & Settings UI:** Improved modal dialogs (delete event, data import) for better viewport fit and readability. Auto-scrolled to the edit form.
- **Today Page:** Redesigned Mood/Pain pills for better visual prominence of data.
- **Tab/Sub-Tab Layout:** Refactored all sub-tab selectors for consistent, mobile-first, and appealing overflow behavior.
- **History Page:** Moved charts to a full-width container for better visibility.
- **Log Page:** Implemented a new week-based, sticky pagination system and updated the log display accordingly.

