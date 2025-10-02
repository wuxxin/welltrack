# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

This update includes a comprehensive set of UI enhancements, feature additions, and behavioral refinements across the application, based on recent user feedback.

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

## Discovered Tasks