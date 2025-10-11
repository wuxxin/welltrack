# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

- **New Prototype for Pain Entry**: Create a new file `prototype/new-pain-entry.html` that mimics the WellTrack GUI's main bar and body pain interface. It will allow selecting body parts, setting pain levels, and highlighting selected parts with the pain level's color. A home icon will reveal a list of created metrics to verify the entry logic.

- **10-Minute Pain Entry Reset**: Implement a feature where the pain entry chart resets after 10 minutes, clearing the visual display of body part inputs (including "pain free") but retaining the metrics.

- **Update Pain Entries within 10 Minutes**: Allow users to change body part entries within a 10-minute window. The old value will be deleted, and a new value will be added to the metrics.

- **Refactor "Pain Free" Button**: Remove the "pain free" button and circle from the SVGs. Implement a new HTML/CSS overlay for the "pain free" selector based on `dev/prototype/pain-free-selector.html`, with new JavaScript logic for selection and unselection.

- **SVG Modifications for Pain Entry**:
  - **Back SVG**: Split the "LWS" (lumbar spine) area vertically. The upper part remains "LWS," and the lower part becomes "KSB" ("Kreuz & Steißbein").
  - **Front SVG**: Split the "brust" (chest) and "bauch" (abdomen) areas into left and right parts.

- **New "Other" Pain Subselector**:
  - Add a new subselector tab labeled "Weitere" (Other).
  - Create an SVG for this view with grouped body parts not on the front/back views, including:
    - A head with selectable left/right ears, left/right eyes, nose, and mouth.
    - Hands with selectable fingers.
    - Feet with selectable toes.
    - A collection for special pains, initially containing "tinitus".

- **"Pain Free" Button Logic**:
  - When the "pain free" button is pushed (and is not already active), reset all pain entries from the last 10 minutes, create a `pain_free_level` metric, and activate the "pain free" indicator.
  - A subsequent click will delete the `pain_free_level` metric and deactivate the indicator.

- **Pain Entry Replacement Logic**: When a pain level is selected, the system will check for any `pain_free_level` or other `pain_bodypart` metrics of the same type within the last 10 minutes. If found, the old entry will be deleted, and the new pain metric will be added.

- **Create GUI Test for Prototype**: Develop a Playwright test to take screenshots of the "back," "front," and "other" views of the new pain entry prototype for verification.

## Completed Tasks

- **Refactor Pain Chart Data Generation (`getPainChartData`)**: Create a new function `getPainChartData` analogous to `getMoodChartData`. It will bucket pain levels from 0 to 5, calculate total pain, and determine a time-weighted average pain (`avg_over_time_pain`).
- **Standardize Time-Weighted Averages**: Refactor both `getMoodChartData` and the new `getPainChartData` to use a consistent, time-weighted average calculation for `avg_over_time`, similar to Prometheus's `avg_over_time`.
- **Update Pain Chart Visualization**: The main pain chart will be updated to show pain levels 0-5 as stacked areas. "Total Pain" and "Average Pain" will be overlaid as line charts. Pain level 0 will be labeled "Schmerz frei" and colored green.

## Discovered Tasks
