# **Planning & Architecture for WellTrack Health Diary**

## **Project Goal**

The primary goal of the WellTrack Health Diary is to provide users with a simple, private, and offline-first Single-Page Application (SPA) to track and visualize personal health data. The application focuses on logging Events, Mood and Pain metrics, and presenting this data in an intuitive and insightful way. The user interface is in German.

## **Current Architecture: Vanilla JS SPA**

The application is implemented as a single-file web application (welltrack.html). This approach maximizes simplicity and portability, requiring no build step.

* **Core Logic:** All JavaScript code is encapsulated within a single global object, WellTrackApp.
* **Structure:** The WellTrackApp object is organized into distinct namespaces for managing different aspects of the application:
    * state: Holds the dynamic application state (e.g., active page, chart instances).
    * config: Stores static configuration, constants, and UI text.
    * data: Handles all interactions with localStorage for data persistence, including CRUD operations and import/export.
    * render: Contains functions responsible for rendering HTML content into the DOM, including pages, components, and charts.
    * events: Manages all user interactions and event listeners.
    * utils: Provides helper functions used throughout the application.
* **Dependencies:** All external libraries (Tailwind CSS, Chart.js, date-fns) are loaded via CDN, eliminating the need for a local build process.

## **Data Structure & Persistence**

* **Storage:** All user data is stored in the browser's localStorage. This ensures privacy (data remains on the user's device) and enables full offline functionality.
    * wellTrackData: An array storing all health metrics.
    * wellTrackTrainings: An array storing user-defined training routines.
    * This storage should the same as data export and import expects for seamless upgrade of HTML page.
* **Data Format:** The health data follows a "Prometheus-like" structure. Each entry is an object with a consistent schema:
    * metric: A string identifying the type of measurement (e.g., pain\_head\_back\_level).
    * timestamp: An ISO 8601 string of when the data was recorded.
    * value: The numerical value of the metric.
    * labels: An object containing key-value pairs that describe the metric (e.g., { "body\_part": "head\_back", "name": "Hinterkopf" }).

## **UI Structure & Components**

The UI is built with Tailwind CSS for responsive, mobile-first design, following Material Design principles for colors and elements. The application is divided into several "pages" that are dynamically rendered into the main container.

* **Pages:**
    * Today: The main dashboard.
    * Events, Mood, Pain: Dedicated data entry pages.
    * History: Chart visualization page.
    * Log: A paginated view of all historical data.
    * Settings: Edit Eventtypes, Import and Export Data.

* **Modals:** A single modal structure is used for various interactions, such as pain level selection, to maintain a consistent user experience.
* **Dynamic Rendering:** Page content and components are generated as HTML strings within the WellTrackApp.render.components object and injected into the DOM using innerHTML. While simple, this approach will be refactored in the future.

## **File Structure**

The project maintains a flat and simple file structure.

Documents:

* system-workflow.md: Development process and coding conventions.
* product-requirements.md: High-level functional and non-functional requirements.
* planning.md: (This file) The architectural and development plan.
* tasks.md: A living document tracking completed tasks, encountered problems and there solution, and planned tasks.
* README.md: A user centric view on howto use the app.

Software and Assets:

* welltrack.html: The main application file containing all HTML, CSS, and JavaScript.
* sw.js: The service worker for PWA caching and offline capabilities.
* manifest.json: The PWA web app manifest.
* icon-192.png / icon-512.png: Application icons.


## **Future Development & Refactoring Plan**

The current vanilla JavaScript implementation serves as a robust prototype. The next major phase will focus on improving maintainability, scalability, and user experience by adopting a modern frontend framework and enhancing native capabilities.

### **Potential Technical Improvements**

* **State Management Library:** Using a library like **Zustand** or **Redux Toolkit** would make state management more robust and traceable.
* **Frontend Framework:** Migrating to a modern framework like **Vue.js**, **Svelte**, or **React** would simplify development with declarative rendering and a component-based structure.
* **Database Backend:** For cross-device synchronization, connecting to a backend like **Firebase Firestore** or **Supabase** would be a significant upgrade over localStorage.
* **Build Process:** A build tool like **Vite** or **Webpack** would enable code minification, modern JavaScript features, and better dependency management.
* **Test Automation:** Introducing unit tests (**Vitest**, **Jest**) and end-to-end tests (**Cypress**, **Playwright**) would improve code quality and long-term stability.

### **Phase 1: Codebase Refactoring**

* **Objective:** Migrate from manual DOM manipulation to a declarative, component-based architecture.
* **Technology Candidates:** **Vue.js**, **Svelte**, or **Alpine.js**. The choice will be based on finding a balance between features and ease of integration into the single-file structure.
* **Steps:**
  1. Introduce the chosen framework via CDN.
  2. Incrementally convert each page (today, pain, mood, etc.) from an innerHTML string to a declarative component.
  3. Replace the WellTrackApp object with a proper state management solution provided by the framework (e.g., Vue's reactivity system, Svelte stores).

### **Phase 2: Enhanced Native Integration**

* **Objective:** Provide a more reliable "app-like" experience, particularly for notifications.
* **Technology:** Wrap the existing PWA using **Capacitor**.
* **Benefits:**
    * **Reliable Notifications:** Implement a native plugin through Capacitor to schedule reliable, persistent notifications that are not dependent on the browser's service worker lifecycle.
    * **App Store Distribution:** This step paves the way for potential distribution through the Apple App Store or Google Play Store.
