# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

## Completed Tasks

- **Refactor Pain Chart Data Generation (`getPainChartData`)**: Create a new function `getPainChartData` analogous to `getMoodChartData`. It will bucket pain levels from 0 to 5, calculate total pain, and determine a time-weighted average pain (`avg_over_time_pain`).
- **Standardize Time-Weighted Averages**: Refactor both `getMoodChartData` and the new `getPainChartData` to use a consistent, time-weighted average calculation for `avg_over_time`, similar to Prometheus's `avg_over_time`.
- **Update Pain Chart Visualization**: The main pain chart will be updated to show pain levels 0-5 as stacked areas. "Total Pain" and "Average Pain" will be overlaid as line charts. Pain level 0 will be labeled "Schmerz frei" and colored green.

## Discovered Tasks
