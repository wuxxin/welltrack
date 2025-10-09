# WorkPad

## New Tasks

Read `dev/system-workflow.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.

required changes:

- add/edit EventType: On Error: missing id or missing naming, or duplicate id, do not abort edit, but resume to edit after error show
- painentry: back and front schmerzfrei circle: sometimes, it is not filled with green if clicked, but the click is still recognized. the next click to unselect works to, but no visible difference. fix this.

- refactor: verlauf: mood chart: add prometheus like avg_over_time to getMoodChartData array adding col "avg_over_time_sum", that is filled with the calculated value. In the diagram add a line diagram on top, thick 3 line, thats a little smoothed. make all area colors more white so it better reflects the colors on other charts. make a screenshot with test data for 7 days, 4 weeks and 3 months range selection.


## nice to have

+ settings: edit event type: add Button (after subtab selector, right aligned just before eventtype list starts) with only an Icon (no text, but hovering reveals "Sortierung verändern", Representing "Loosing Chains" for reorder, and "closed Chains" as the other icon once in reorder mode to freeze changes. clicking "Reorder" Icon blurs everything except the event type list, that gets grab icons on the left, and disables/greysout (modal type) all other user interface, so only the list and the icon "Closed Chains" are clickable, the user can reorder the event types, and either abort (clicked outside) aborts the reordering, or the click on "closed Chain" freezes the new reordering, after the metrictype array gets resorted from the dom order. testcase: add sample data, make screenshot of settings:eventtypes original order, press reorder, take screenshot, reorder third to first, fifth to second, take screenshot, press lock, screenshot.

+ body pain entry tab: body: new subselector (additional to back and front) other: other "Weitere" is a svg like front and back with "SchmerzFrei" as on the other svg's , but with selected bodyparts that are grouped for detailed not covered on front and back parts, eg: ears, eyes, nose, mouth, fingers , toes, and some special "pain" like "tinitus" seperated.

+ Gui Translation
    make translations that are inside welltrack.html and are selected automatically on browser agent preferences, and switchable in settings "Darstellung" "Sprache", "Default", "Deutsch", "English", defaulting to "default" which uses the browser preferred language, if available, or English if not available.

+ Gui Dark Theme
    +make an additional dark theme, add switch to settings after Erinnerungen, "Darstellung", "Design", "Hell | Dunkel" , default hell

+ Gui browser Forward/Back Utilization
    make browser forward and browser back work as go through recorded selected subtabs, eg. clicked on today, mood, go to mood entry, click browser back, return to today.

+ Gui Icon-Bar Placement
    make icon bar switchable between up and down location, add switch to settings, after "Erinnerungen", "Darstellung" , "Menübalken" "Oben" | "Unten", default "Oben"


### Document Tasks

Your task is to thoroughly document this entire repository. Please follow these steps meticulously:

Read dev/system-workflow.md, dev/product-requirements.md, dev/project-structure.md, README.md, and src/welltrack/welltrack.html.

Full Docstring Coverage: Systematically scan every source file. Add a complete docstring to every single public function, method, and class. Do not skip any, regardless of their apparent simplicity.

High-Quality Docstrings: For each docstring, ensure you clearly explain:

The purpose or main action of the code.
A description for every parameter/argument.
A description of the return value.
Follow Conventions: Adhere to the standard documentation style for the repository's programming language (e.g., JSDoc, Google Style Python Docstrings, GoDoc).

Update or create dev/project-structure.md: Review and update to be a complete guide for a new developer, covering purpose, setup, build and usage. Describe The Data Architecture, the different ind of metric entries, time based value entries, push button events, and mood and pain entries that have moving 10min timeslots, the export format, and each gui tab for what it displays.
