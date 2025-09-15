# **Tasks**

This document lists the implementation status of features and refactorings for the WellTrack health diary app.

## **Implemented Features (Completed)**

* \[x\] **Core SPA Structure:** Implemented page-based navigation (Today, Events, Mood, Pain, History, Log).
* \[x\] **PWA Functionality:** App is installable, works offline, and has notification permission requests.
* \[x\] **"Today" Dashboard:** Main page shows a daily summary with comparison to the previous day and a detailed log.
* \[x\] **Events Logging:** Dedicated "Events" page for recording duration for predefined sessions.
* \[x\] **Interactive Mood Logging:** Implemented a dedicated "Mood" page with grouped, switchable mood categories and 0-5 sliders.
* \[x\] **Interactive Pain Logging:** SVG body graphic with clickable regions on a dedicated "Pain" page.
* \[x\] **Data Persistence:** Saving and loading all data in the browser's localStorage.
* \[x\] **Enhanced History View:** Integration of Chart.js with stacked bar charts for all metrics (including an additive mood chart) and improved Y-axis scaling.
* \[x\] **Enhanced Log View:** The full log now displays daily totals for all metrics and detailed breakdowns.
* \[x\] **Time Filter:** Ability to filter the displayed time range in the history charts (7/30/180 days).
* \[x\] **Events Management:** Adding, editing, and deleting custom Events types via a settings modal.
* \[x\] **Data Import/Export:** Implementation of the export and import functionality as a JSON file.
* \[x\] **Responsive Design:** Ensured usability on mobile devices and desktops using Tailwind CSS.

## **Future Tasks (Planned)**

* make the "verlauf" subtab buttons look and behave like the mood-subtab buttons
* events get a new feature: if increment = 0 it becomes a timestamp only button (with an undo function) for eg. Medication Intake , where only time and that it happens is important, in the event entry page.
* clarify the event edit tab to tip the user un the time stamp only feature with 0 increment.
* create sub Events tabs like sub mood tabs.
    * "+min" positive increments (eg. 1,15) types of the same unit (min)
    * "-min" negative increments of the same unit (min)
    * "-habbit" 0 increment of unit type -habbit
    * "+habbit" 0 increment of unit type +habbit
    * "habbit" 0 increment of any unit type
    * "*" for other
* make verlauf stimmung only display the culmulative chart with all the negativ cummulativ and the positive cumulative together.
    * the tooltip should reveal the mood detauk data of the cumulative data bar.
* give all verlauf diagrams an good looking moving average. mavg for 7 days should be 3 , 7 for 30 and 28 for 180
*
* \[ \] **Refactoring: State Management & Frontend Framework**
    * \[ \] Migration of the entire application logic and state management from the WellTrackApp object to a more robust solution like **Alpine.js**, **Vue.js**, or **Svelte**.
    * \[ \] Conversion of manual DOM manipulations (innerHTML assignments) to declarative directives/components.
* \[ \] **Reliable Native Notifications:** For a full mobile app experience, implement reliable, scheduled notifications by wrapping the PWA in a native container like **Capacitor**.

