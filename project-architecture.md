# **Project Architecture: WellTrack Health Diary**

This document describes the architecture of the WellTrack Single-Page Application (SPA). It is divided into a description of the features from a user's perspective, the technical features, and the implementation architecture, including potential improvements.

## **1\. Features from a User's Perspective**

The application offers users a simple and intuitive way to record and visualize health-related data. Its User Interface language is German.

### **Core Pages & Navigation**

The app is structured into several main pages for clear separation of concerns:

* **Today (Homepage):** A dashboard providing an at-a-glance summary of the current day's metrics. It displays total pain, training duration, and mood scores, along with a comparison to the previous day's totals to highlight trends. A detailed log of all entries from the current day is listed below the summary.
* **Entry Pages (Training, Mood, Pain):** Dedicated pages for data input. Users can navigate to each page via icons in the header to log specific metrics for the current day.
* **History (Charts):** A visualization page showing trends over time for pain, mood, and training data in stacked bar charts.
* **Full Log:** A paginated, chronological list of all recorded data, grouped by day.
* **Settings:** A modal for managing training routines and app settings like data import/export and notification permissions.

### **Main Functions**

* **Pain Logging:**
  * On the dedicated "Pain" page, users can select specific body parts on an interactive representation of the human body (front and back views).
  * For each selected part, the pain intensity can be recorded on a scale from 0 (no pain) to 5 (excruciating).
* **Mood Logging:**
  * On the "Mood" page, users rate various aspects of their mood on a 0 (most negative) to 5 (most positive) scale using visual sliders.
  * Moods are organized into switchable groups (e.g., "Energy & Motivation", "Well-being & Self-Esteem").
* **Training Logging:**
  * On the "Training" page, users can log completed training sessions for the current day.
  * The duration of each session can be adjusted in 15-minute increments.
  * The app highlights training sessions that are scheduled for the current day but not yet completed.
* **Graphical History:**
  * The "History" view visualizes collected data in stacked bar charts, allowing users to see the composition of their metrics each day.
  * There are separate charts for total pain (stacked by body part), total mood (stacked by mood type), and total training duration (stacked by activity).
  * The displayed time range can be filtered (last 7, 30, or 180 days).
  * All charts feature a detailed Y-axis with at least 8 steps for better readability.
* **Full Log View:**
  * The "Full Log" provides a detailed historical record.
  * Each day's entry displays total scores for pain, training, and mood.
  * A detailed breakdown for each metric (e.g., individual pain points, specific mood ratings with color codes) is shown for each day.
* **Training Management:**
  * Users can create, edit, and delete custom training routines in the settings modal.
* **Data Import & Export:**
  * All data and settings can be exported to a single JSON file for backup and restored via an import function.

## **2\. Technical Features**

* **Progressive Web App (PWA):** The application includes a Service Worker and a Web App Manifest, allowing it to be "installed" on a mobile device and function offline. It also includes the basic framework for push notifications.
* **Single-Page Application (SPA):** The entire application is loaded in a single HTML file. Navigation between pages is handled dynamically with JavaScript without page reloads.
* **Local Data Storage:** All user data is stored in the browser's localStorage, enabling fast, offline-capable usage without a backend.
* **Dependencies via CDN:** All external libraries (Tailwind CSS, Chart.js, date-fns) are included via a Content Delivery Network (CDN), simplifying setup.
* **Responsive UI:** The layout, built with Tailwind CSS, adapts to various screen sizes.
* **Interactive Data Visualization:** Chart.js is used to generate interactive and customizable bar charts.
* **Prometheus-like Data Format:** Data is stored as an array of metric objects, each with a metric name, timestamp, value, and descriptive labels.

## **3\. Implementation Architecture & Improvements**

The entire JavaScript code is encapsulated in a single global object, WellTrackApp, structured into logical sub-objects (state, config, data, render, events, utils).

### **Potential Technical Improvements**

1. **State Management Library:** Using a library like **Zustand** or **Redux Toolkit** would make state management more robust and traceable.
2. **Frontend Framework:** Migrating to a modern framework like **Vue.js**, **Svelte**, or **React** would simplify development with declarative rendering and a component-based structure.
3. **Database Backend:** For cross-device synchronization, connecting to a backend like **Firebase Firestore** or **Supabase** would be a significant upgrade over localStorage.
4. **Build Process:** A build tool like **Vite** or **Webpack** would enable code minification, modern JavaScript features, and better dependency management.
5. **Test Automation:** Introducing unit tests (**Vitest**, **Jest**) and end-to-end tests (**Cypress**, **Playwright**) would improve code quality and long-term stability.