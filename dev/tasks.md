# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- **GUI Dark Theme:**
  - Create an additional dark theme.
  - Add a switch to settings under "Darstellung" -> "Design" with options "Automatisch | Hell | Dunkel".
  - Default to "Automatisch", which uses browser preference, falling back to "Hell".
  - Clean up unused CSS.
  - Create a test to screenshot all main screen tabs with sample data in both dark and light modes.
  - Save screenshots to `build/tests/output`.
  - Show the user the generated screenshots.

- **Font Size Slider:**
  - Add a "Schriftgröße" slider in "Settings" -> "Darstellung".
  - Range from 50% to 200%, defaulting to 100%.
  - The slider should change `body { font-size }`.

## Discovered Tasks
