# **Tasks**

This document lists the implementation status of features and refactorings for the WellTrack health diary app.

## **Implemented Features**

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

## **Resolved Problems and Solutions**


## **Planned Tasks**

* make the local storage data equal to the export data, so on every keypress, the data that would be created on export will be stored to local storage,
so an update to the underlying webpage, can read the local storage because its equal to an import

* Add a new button (checkmark and +1) next to "Stimmung" on mood entry tab, and next to Vorderseite/Rückseite on pain tab, that is greyed out if no data is entered so far, but can be pressed, once any mood or pain data is entered. if pressed, the last entries are finished and a new entry (for the same day, but different data) is begun.
  this is in addition to the reset values on day change automatic, where all values (events, mood, pain) reset. This does not change the events counted for this day.

* make the "verlauf" subtab buttons look and behave like the mood-subtab buttons

* events get a new feature: if increment = 0 it becomes a timestamp only button (with an "undo" function and a "reload" function) for eg. Medication Intake , where only time and that it happens is important, in the event entry page. Reload can only be pressed if it is already pressed for today, and makes a new press possible. undo is only pressable if already pressed, and undos the last pressing.
* event types are getting a group type (default empty).

* create sub Events tabs like sub mood tabs.
    * for every group type, list all events of this group type with naming if grouptype
    * add "*" for events without (empty) grouptype

* Verlauf Page:
    * Add a (cummulative) chart for events on of same grouptype and unittype
    * Add a chart for every other grouptype and equal unittype
    * Add single charts for all other events

* change all verlauf diagrams from bars to linechar, make a good looking moving average. mavg for 7 days should be 3 , mavg for 30 should be 7 , mavg for 180 shoould be 28

* make verlauf mood only display the culmulative Candle with all the negativ cummulativ and the positive cumulative together.
    * the tooltip should reveal the mood detault data of the cumulative data bar.

