# WorkPad

## New Tasks

Read `dev/system-workflow.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.

required changes:


- pain entry: quirks with pain_free and pain_body part entries, does not fill parts or painfree circle when pressed, its recorded but not displayed.

- refactor pain charts: create getPainChartData(pain_mod="linear") in analog to getMoodChartData(), but with the following differences: buckets are pain_0 to pain_5 (as pain values can be), total_pain, avg_over_time_pain)
    - refactor both getmoodchardata and getpainchartdata that the avg_over_time from total_pain/total_mood is equally to avg_over_time in prometheus. if this is to complicated, think of a thirdparty library available over cdn to include.
    - refactor pain chart: first chart will be similar to moodchart: pain_0 to pain_5 are stacked area, total_pain and avg_over_time_pain are lines on top of areas, and are not stacked or interacting. because of the getpainchartdata time normalizing to 10min slots, we can use similar tooltip settings.  Label the pain_0 to pain_5 like the pain selection text, except pain_0, please label it "Schmerz frei", use the same colors for pain_1 to pain_5, for pain_0 use green.


## nice to have

- settings: edit event type: add Button (after subtab selector, right aligned just before eventtype list starts) with only an Icon (no text, but hovering reveals "Sortierung verändern", Representing "Loosing Chains" for reorder, and "closed Chains" as the other icon once in reorder mode to freeze changes. clicking "Reorder" Icon blurs everything except the event type list, that gets grab icons on the left, and disables/greysout (modal type) all other user interface, so only the list and the icon "Closed Chains" are clickable, the user can reorder the event types, and either abort (clicked outside) aborts the reordering, or the click on "closed Chain" freezes the new reordering, after the metrictype array gets resorted from the dom order. testcase: add sample data, make screenshot of settings:eventtypes original order, press reorder, take screenshot, reorder third to first, fifth to second, take screenshot, press lock, screenshot.

- body pain entry tab: body: new subselector (additional to back and front) other: other "Weitere" is a svg like front and back with "SchmerzFrei" as on the other svg's , but with selected bodyparts that are grouped for detailed not covered on front and back parts, eg: ears, eyes, nose, mouth, fingers , toes, and some special "pain" like "tinitus" seperated.

- welltrack_lab: add function of a lab thats sole purpose is to analyze data gathered from welltrack.html. Icon to create from create-sample-data.py , icon to open/import from user, icon to download/save to user, make all data in json metrics, eventtypes, settings available, and editable.
    - automatic creation of timeslot sum for pain and mood values, bucket pain values, bucket mood values, make timebased average on switchable eventType,
    - make day to day mood/pain/eventtype comparison charts, day of week to day of week, whole 4 weeks to another 4 weeks with aligned dayofweek.
    - correlation study: chart to visualize how mood entry values of one mood question are correlated to another
    - make bar charts for group, pain, mood to display percentage of value of a group, of a mood, of a pain in the total.
    - make pushbutton entries overlayable to any chart (eg. take a medication)
    - use any modern tool availabel in the techstack (see `pyproject.toml`) but any pure python or python package supported by pyodide (for wasm support in the marimo welltrack lab) is ok.

- Gui Translation
    make translations that are inside welltrack.html and are selected automatically on browser agent preferences, and switchable in settings "Darstellung" "Sprache", "Default", "Deutsch", "English", defaulting to "default" which uses the browser preferred language, if available, or English if not available.

- Gui Dark Theme
    +make an additional dark theme, add switch to settings after Erinnerungen, "Darstellung", "Design", "Hell | Dunkel" , default hell

- Gui browser Forward/Back Utilization
    make browser forward and browser back work as go through recorded selected subtabs, eg. clicked on today, mood, go to mood entry, click browser back, return to today.

### Document Tasks

Your task is to thoroughly document this entire repository. Please follow these steps meticulously:

Read dev/system-workflow.md, dev/product-requirements.md, dev/development.md, README.md, and src/welltrack/welltrack.html.

Full Docstring Coverage: Systematically scan every source file. Add a complete docstring to every single public function, method, and class. Do not skip any, regardless of their apparent simplicity.

High-Quality Docstrings: For each docstring, ensure you clearly explain:

The purpose or main action of the code.
A description for every parameter/argument.
A description of the return value.
Follow Conventions: Adhere to the standard documentation style for the repository's programming language (e.g., JSDoc, Google Style Python Docstrings, GoDoc).

Update or create dev/development.md: Review and update to be a complete guide for a new developer, covering purpose, setup, build and usage. Describe The Data Architecture, the different ind of metric entries, time based value entries, push button events, and mood and pain entries that have moving 10min timeslots, the export format, and each gui tab for what it displays.
