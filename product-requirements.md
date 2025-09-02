# **Project Architecture: Pain and Mood Diary**

This document describes the architecture of the Pain and Mood Diary Single-Page Application (SPA). It is divided into a description of the features from a user's perspective, the technical features, and the implementation architecture, including potential improvements.

## **1\. Features from a User's Perspective**

The application offers users a simple and intuitive way to record and visualize health-related data.
Its User Interface language is german.

### **Main Functions**

* **Pain Logging:**
  * Users can select specific body parts on an interactive, representation of the human body, which can be switched (eg. front , back or head only).
  * For each selected part, the pain intensity can be recorded on a scale from 0 (no pain) to 5 (excruciating).
  * The recorded pain for the current day is visualized with colors on the body diagram.
* **Mood Logging:**
  * Users can enter a selectable list of mood descriptors , each list has negativ and positive pairs, that scale between 0 (the most negativ to 5 the most positiv)
* **Logging Training Sessions:**
  * Users can log completed training sessions for the current day.
  * The duration of each session can be increased or decreased in 15-minute increments.
  * The app indicates if a training session scheduled for today is still pending.
* **Graphical History:**
  * A history view visualizes the collected data in charts.
  * There are separate graphs for pain intensity (stacked by body part), mood intensity (stacked) and training duration (stacked by training type).
  * The displayed time range can be filtered (last 7 days, 30 days, 6 months).
  * Tooltips in the charts display dates in a condensed format for clarity.
* **Training Management:**
  * Users can create new, custom training types.
  * Existing trainings can be edited (name, planned duration, days of the week) or deleted.
  * The user interface for managing trainings is contained within a settings modal, with sub-menus for editing or creating that return the user to the main settings view upon completion.
* **Data Import & Export:**
  * All recorded data (pain, training) and the configured training types can be exported into a single JSON file.
  * This format is inspired by Prometheus and serves for easy data backup and migration.
  * A previously exported JSON file can be imported to restore the app's state.

## **2\. Technical Features**

The application is designed as a self-contained HTML file that does not require a server-side component.

* **Single-Page Application (SPA):** The entire application is loaded in a single HTML file. Navigation between views (Diary, History) is handled dynamically with JavaScript without reloading the page.
* **Local Data Storage:** All user data is stored directly in the browser's localStorage. This allows for fast, offline-capable usage without the need for a backend or an internet connection.
* **Dependencies via CDN:** All external libraries (Tailwind CSS, Chart.js, date-fns) are included via a Content Delivery Network (CDN). This simplifies the setup as no local installation or build process is required.
* **Responsive User Interface:** The layout is built with Tailwind CSS and flexibly adapts to different screen sizes, from mobile devices to desktops.
* **Interactive Data Visualization:** The Chart.js library is used to display the historical data, generating interactive and customizable bar charts.
* **Prometheus-like Data Format:** The data is stored in an array of metric objects. Each object contains a metric name (e.g., pain\_head\_front\_level), a timestamp, a value, and descriptive labels. This structured format facilitates analysis and export.
* **idnames comments in sourcecode and any documentation markdown are in english.

## **3\. Implementation Architecture & Improvements**

The entire JavaScript code is encapsulated in a single global object, TagebuchApp, to keep the global namespace clean. This object is structured into logical sub-objects.

### **Code Structure (TagebuchApp Object)**

* **state**: Stores the current state of the application, e.g., which page is active (activePage), which body part is currently being edited (currentPainPart), or references to the chart instances.
* **config**: Contains static configuration values that control the app's behavior, such as pain level definitions, the number of entries per page, or color definitions.
* **data**: Bundles all functions for reading, writing, and migrating data from localStorage. The import/export logic is also implemented here.
* **render**: Contains all functions responsible for creating and updating the HTML DOM. It is further divided into:
  * render.pages: Generates the main views (Diary, History).
  * render.modal: Controls the display and content of modal windows.
  * render.components: Contains functions that generate reusable HTML snippets (components), e.g., for a training item or a log entry.
  * render.charts: Responsible for creating and updating the charts with Chart.js.
* **events**: Defines all the application's event handlers. These functions react to user interactions (e.g., clicks), call the appropriate data and render functions, and update the state.
* **utils**: A collection of helper functions that are reused in various parts of the application (e.g., date formatting, color generation, text slugification).

### **Potential Technical Improvements**

1. **State Management Library:** Instead of a simple state object, a small state management library (e.g., **Zustand** or **Redux Toolkit**) could be introduced. This would make managing the application state more robust and traceable as complexity grows.
2. **Frontend Framework:** Manual DOM manipulation is error-prone. Migrating to a modern frontend framework like **Vue.js**, **Svelte**, or **React** would significantly simplify and accelerate development through declarative rendering, a component-based structure, and a reactive data model.
3. **Database Backend:** localStorage is limited to about 5 MB and is not suitable for synchronization between devices. A possible extension would be to connect to a backend with a database (e.g., **Firebase Firestore** or **Supabase**). This would enable cross-device synchronization, user logins, and more secure data storage.
4. **Build Process:** Including libraries via CDN is simple, but for a production application, a build process (e.g., with **Vite** or **Webpack**) is advantageous. It allows the use of modern JavaScript features, code minification, CSS preprocessors, and better dependency management.
5. **Test Automation:** Introducing unit tests (e.g., with **Vitest** or **Jest**) for the logic in data and utils, as well as end-to-end tests (e.g., with **Cypress** or **Playwright**), would ensure code quality and stability in the long run.