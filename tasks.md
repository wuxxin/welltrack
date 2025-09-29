# **Tasks**

This document lists the implementation status of features and refactorings for the WellTrack health diary app.

## **Implemented Features**

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
- [X] **Mood Entry:** Prevented mood ruler clicks during page scroll by distinguishing between click and drag events.
- [X] **Today Page:**
    - [X] Redesigned header to split "Heute" and the date for better readability.
    - [X] Redesigned summary cards to be more compact, space-efficient, and visually informative.
- [X] **Event Entry:** Improved layout of event items to fit on a single line, even on smaller screens.
- [X] **History Charts:**
    - [X] Set a height of 600px for all charts.
    - [X] Reverted dynamic width scaling for charts, maintaining a consistent 100% width.
- [X] **Log Page (Protokoll):**
    - [X] Made log cards wider with a larger base font size for better readability.
    - [X] Restructured the card layout with the date positioned in the top-right, in the normal content flow.
    - [X] Implemented a structured matrix/grid display (3-4 columns) for Mood and Pain sub-metrics.
    - [X] Applied consistent color-coding to all relevant values.
    - [X] Hid timestamps for incrementing (non-timestamp) events.
    - [X] Re-formatted timestamp events to "Um hh:mm: [Event Name]".

## **Resolved Problems and Solutions**

## **New Tasks**

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

## **Planned Tasks**

