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

## **Resolved Problems and Solutions**


## **Planned Tasks**
