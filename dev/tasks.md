# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- **[x] Refactor `console.log()` with `rebirth_message` overlay**: Replace `console.log()` calls next to `location.reload()` with a mechanism to save a `rebirth_message` to settings. This message will be displayed in an overlay on the next page load, similar to the version overlay, and must be ableto be displayed simultaneously with the version overlay.

- **[x] Feature: "Heute = 05-05" Day Logic**:
    - Redefine a "day" to run from 5:00 AM to 4:59 AM the next calendar day.
    - Update the "Today" page to display "Heute -> Montag auf Dienstag" between midnight and 5:00 AM.
    - Ensure daily value resets (e.g., for events) occur at 5:00 AM.
    - Push button values should show counts from the current WellTrack day (e.g., "3x last 03:30") and allow undoing into the previous calendar day if it's the same WellTrack day.

- **[x] Feature: Protokoll (Log) Refactor**:
    - Rewrite the data gathering logic for the Protokoll to align with the new 5-to-5 day definition.
    - For mood and pain entries, group all values within a 10-minute window into a single block, using the timestamp of the first entry.
    - Within each block, the individual mood/pain items should be serialized and sorted by name.
    - The final array of blocks for the day should be reversed to show the latest entries first.

## Discovered Tasks