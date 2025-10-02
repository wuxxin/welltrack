# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

This update includes a comprehensive set of UI enhancements, feature additions, and behavioral refinements across the application.

- **UI & Styling:**
  - Redesigned "Today" tab pills for mood, pain, and events to improve readability and handle long text. The "gleichbleibend" trend indicator now correctly uses a right-arrow icon and an equals sign. Event pills now default to a horizontal layout and wrap vertically when needed.
  - Cleaned up the "Event Entry" tab by reorganizing buttons to appear on the same line as the event name when space permits.
  - Standardized all tab and section heading sizes for a consistent look and feel.
  - Adjusted subgroup selectors on the "Event Entry" and "Verlauf" tabs to wrap and align to the right on smaller screens.
  - Adjusted history chart data aggregation to ensure daily bars render correctly and removed the moving average line for clarity.

- **Features & Logic:**
  - Implemented a "Pain-Free" button on the pain entry screen to allow users to log periods of no pain.
  - Refined the mood slider to prevent accidental selections when scrolling.
  - Updated the "delete event type" logic to count existing entries, display a detailed confirmation message, and delete both the event type and its associated data.
  - Refactored the `is_cumulative` field into a new `displayType` setting with three options ("Zusammenzählen," "Einzeln, hervorheben," "Einzeln") to control how events are grouped and displayed.
  - Enhanced the data import/merge functionality to prevent overwriting existing event configurations and to reconstruct metric labels based on current app settings.

## Discovered Tasks