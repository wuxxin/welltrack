# **Tasks**

This document lists the implementation status of features and refactorings for the Pain and Mood Diary app "welltrack"

## **Implemented Features (Completed)**

* \[x\] **Basic SPA Structure:** Implemented navigation between the diary and history views.
* \[x\] **Interactive Pain Logging:** SVG body graphic with clickable regions and a modal for pain input.

* \[x\] **Training Logging:** Recording the duration for predefined training sessions.
* \[x\] **Data Persistence:** Saving and loading all data in the browser's localStorage.
* \[x\] **History View:** Integration of Chart.js for visualizing pain and training data.
* \[x\] **Time Filter:** Ability to filter the displayed time range in the graphs (7/30/180 days).
* \[x\] **Training Management:** Adding, editing, and deleting custom training types.
* \[x\] **Data Import/Export:** Implementation of the export and import functionality as a JSON file.
* \[x\] **Responsive Design:** Ensured usability on mobile devices and desktops using Tailwind CSS.

## **Future Tasks (Planned)**

* \[ \] **Interactive Mood Logging:** clickable regions to select between most negativ = 0 and most positive = 5 so 6 states for mood input
* \[ \] **Refactoring: State Management & Frontend Framework**
  * \[ \] Migration of the entire application logic and state management from the TagebuchApp object to **Alpine.js**.
  * \[ \] Conversion of manual DOM manipulations (innerHTML assignments) to declarative Alpine.js directives (x-data, x-for, x-show, etc.).