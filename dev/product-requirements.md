# Product Requirements for WellTrack Health Diary

## Introduction & Objective

This document describes the architecture of the WellTrack Single-Page Application (SPA). It is divided into a description of the features from a user's perspective, the technical features, and the implementation architecture, including potential improvements.

## System Overview

The application offers users a simple and intuitive way to record and visualize health-related data. Its User Interface language is German.

## Functional Requirements

The app is structured into several main pages for clear separation of concerns:

- **Today (Homepage):** A dashboard providing an at-a-glance summary of the current day's metrics. It displays total events, mood and pain scores, along with a comparison to the previous day's totals to highlight trends. A detailed log of all entries from the current day is listed below the summary.
- **Entry Pages (Events, Mood, Pain):** Dedicated pages for data input. Users can navigate to each page via icons in the header to log specific metrics for the current day.
- **History (Charts):** A visualization page showing trends over time for Events, Mood and Pain data in stacked bar charts.
- **Full Protocol:** A paginated, chronological list of all recorded data, grouped by day.
- **Settings:** managing Event types and app settings like data import/export and notification permissions.

### Main Functions

- Events Logging:
    - On the "Events" page, users can log Events for the current day.
- Mood Logging:
    - On the "Mood" page, users rate various aspects of their mood on a -3 (most negative) to +3 (most positive) scale using visual sliders.
    - Moods are organized into switchable groups (e.g., "Energy & Motivation", "Well-being & Self-Esteem").
- Pain Logging:
    - On the dedicated "Pain" page, users can select specific body parts on an interactive representation of the human body (front and back views).
    - For each selected part, the pain intensity can be recorded on a scale from 0 (no pain) to 5 (excruciating).
- Graphical History:
    - The "History" view visualizes collected data in stacked bar charts, allowing users to see the composition of their metrics each day.
    - There are separate charts for total pain (stacked by body part), total mood (stacked by mood type), and total Events duration (stacked by activity).
    - The displayed time range can be filtered (last 7 days, 4 weeks or 3 months (84 days)).
- Full Protocol View:
    - The "Full Protocol" provides a detailed historical record.
    - Each day's entry displays total scores for events, mood and pain.
    - A detailed breakdown for each metric (e.g., individual pain points, specific mood ratings with color codes) is shown for each day.
- Settings View:
    - Event Types Management: Create, edit, and delete EventTypes
    - Data Import & Export: All data and settings can be exported to a single JSON file for backup and restored via an import function.
    - Notification configuration
    - Appearance: Start of the Day Configuration, defaults to 05:00
    - About App: A brief about page with linsk to the sourcecode

## Non-Functional Requirements / Technical Features

- **Progressive Web App (PWA):** The application includes a Service Worker and a Web App Manifest, allowing it to be "installed" on a mobile device and function offline. It also includes the basic framework for push notifications.
- **Single-Page Application (SPA):** The entire application is loaded in a single HTML file. Navigation between pages is handled dynamically with JavaScript without page reloads.
- **Local Data Storage:** All user data is stored in the browser's localStorage, enabling fast, offline-capable usage without a backend.
- **Prometheus-like Data Format:** Data is stored as an array of metric objects, each with a metric name, timestamp, value, and descriptive labels.
- **Easy Update:** All user data stored in the browser's localStorage is equivalent to the Prometheus-like Data Format used for import and export, allowing seamless upgrade of the single HTML file.
- **Dependencies via CDN:** All external libraries (Tailwind CSS, Chart.js, date-fns) are included via a Content Delivery Network (CDN), simplifying setup.
- **Responsive UI:** The layout, built with Tailwind CSS, adapts to various screen sizes and is designed as mobile first.
- **Interactive Data Visualization:** Chart.js is used to generate interactive and customizable bar charts.
- **Implementation Architecture** The entire JavaScript code is encapsulated in a single global object, WellTrackApp, structured into logical sub-objects.
