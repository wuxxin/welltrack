# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- **Settings: Event Type "Nur Aufzeichnen"**: Added a new display type for events, "Nur Aufzeichnen". Events of this type are recorded but not included in daily summaries or historical charts.

- **Protokoll Sorting and Refactoring**: Sorted the daily entries in the log (both on the full log page and the "Today" page) with the newest entries appearing first. The sorting order is: pushbuttons, other timestamped events, mood entries, and finally pain entries. Removed the `ENTRIES_PER_PAGE` constant.

- **Update Notification System**: Implemented a system to notify users of application updates. This involves checking the last modified date of `welltrack.html`, displaying an overlay with the new version details upon update, and storing this version information in settings.

- **Event Type Editor as Modal**: Converted the event type editor in the settings from an inline form to a modal overlay. The modal is responsive and includes options to save or abort changes.

- **Reorder Event Types**: Added a feature to allow users to reorder the list of event types. This includes a dedicated "reorder" mode with drag-and-drop functionality and a mechanism to save the new order.

## Discovered Tasks
