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


## **Planned Tasks**

### 2025-09-23
- [ ] Change all epoch seconds to standard epoch milliseconds in `welltrack.html` for consistency.
- [ ] Repair `create_sampledata.py` to ensure all body parts, moods, and standard event types are sourced directly from `welltrack.html`.
- [ ] Update `create_sampledata.py` to generate timestamps in milliseconds.
- [ ] Update this file (`tasks.md`) to reflect the work done.
