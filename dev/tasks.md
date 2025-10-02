# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

This update includes a comprehensive set of UI enhancements, feature additions, and behavioral refinements across the application.

- **UI & Styling:**
  - **Today Page:**
    - Pain trend indicator: up-arrow in red for increased pain, down-arrow in green for decreased pain.
    - "Letzte Einträge" section will be collapsible with a horizontally centered button, hidden by default.
  - **Settings Page:**
    - Implement sub-tabs: "Ereignisarten", "Datenverwaltung", "Erinnerungen", "über".
    - The selected sub-tab will be remembered.
  - **Sub-tab Selector Alignment:**
    - On "Stimmung" and "Schmerzen" tabs, the sub-tab selector will be on the same line as the title and right-aligned.
    - On the "Verlauf" tab, the selector will move down and to the right when pressured.
  - **Protokoll Page:**
    - Pagination buttons ("zurück", "weiter") will be styled like the "Neue hinzufügen" button.
    - After pagination, the view will scroll to the new end of the page.

## Discovered Tasks