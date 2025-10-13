# WorkPad

## New Tasks

Read `dev/system-workflow.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.

required changes:

- make a new prototype in `dev/prototype/new-pain-entry.html`:

create a skeleton welltrack gui mainbar, tailwind css, mimicking the welltrack app but only the body pain part interface is exposed. a click on the home icon reveals a list of currently created metric with time and metricname value to verify working entry logic. refaktor out the body svg's and selection. it should be able to select body parts, select the pain level, and highlight the already set body_parts in the color of the pain level, and record the pain entries to an array equal to welltrack.

- the pain entry chart resets (as welltrack) afer 10min and resets all body part input to zero (including pain_frree) for the display, but the metrics are kept.
- within a 10 minute period (as welltrack) it is possible to change body part entries, by assigning them a new value. the old value is looked up, deleted, and a new value is added on top of the metrics, like in welltrack.

- pain entry back svg: split "LWS" vertically, upper part remains LWS, lower part becomes "KSB" with long german text "Kreuz & Steißbein", remove pain_free.
- pain entry front svg: split "brust" und "bauch" to left and right part. remove pain_free.
- new subselector: other named "Weitere". A list in two cols, of user created special pain entry possibilities, but the first item on the list is alway the new "pain free" item. use the `dev/prototype/pain-free-selector.html` "Body Icon" for "'BodyIcon Schmerz Frei" as title of first item. other items are generated from the list of extra painTypes a new array similar to eventTypes, but for custom pain entries: eg. '{"pain_id": "english_clear_name", name="German Common Name"}'. for this demo assume two custom Entries, "Tinitus" and "Sodbrennen", give tinitus title a fitting icon in the title, equal for sodbrennen, so its displayed "icon titlename" . if pressed they behave like other body pain parts, they become filled with the pain value color, and a welltrack metric is generated.

- on init, any body/pain part that should be colored, look metrics latest to earlier within the last 10 minutes for pain entries add each color value found with the level. if any pain_free_level or 10 min is encountered further processing is stopped.

- if any pain that is clicked, it looks within the last 10 minutes (latest to earlier) of pain entries if there is a pain_free_level or another pain_bodypart metric of the same type that would be replaced with the new value, then delete the old entry (pain_free_level, or the old pain_bodypart metric), attach a new entry with the new pain metric.

- if "pain free" button is selected, it looks if there are set pain parts in the last 10 minutes, and if so it asks with a modal, "wieder Schmerzfrei ?" "Nein" und "Ja", if "ja" it goes back 10 minutes, and removes all pain entries from their to now. it then adds the pain_free metric, and colors the button if there was no question or the question was answered with ja.

- create a test in tests that uses this prototype to take screenshots from painentry: back, front and other tab.


---
Read `dev/system-workflow.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.

required changes:

- fix: gui:on a evententry pushbutton the layout still flickers around a pixel for unselected and selected pushbutton.

- Gui Dark Theme:
    - make an additional dark theme, add switch to settings after Erinnerungen, "Darstellung", "Design", "Automatisch | Hell | Dunkel" , default automatic, automatic selects depending user browser preference, if that fails "hell".
    - while making the theme, look for any css that is not used or could be cleaned out before implementing it in dark mode. go over any css and think if it needs to change for dark mode. correlate background (blackish) with foreground whiteish, maintain a good contrast like in the bright theme. make sure most backgrounds in dark mode are blackish or darkish, but not bright. adjust the content inside of these containers.
    - to be sure that all of the theme is correct a number of screenshots must be made and visualy analyzed.
        - make this a test in `tests/test_darktheme.py` that screenshots to (mkdir) `build/tests/darktheme` with of all main screen tabs with sample data, both in dark mode and in bright mode, and then looks at each output and looks if it is correct for the theme.


## nice to have

- settings: edit event type: add Button (after subtab selector, right aligned just before eventtype list starts) with only an Icon (no text, but hovering reveals "Sortierung verändern", Representing "Loosing Chains" for reorder, and "closed Chains" as the other icon once in reorder mode to freeze changes. clicking "Reorder" Icon blurs everything except the event type list, that gets grab icons on the left, and disables/greysout (modal type) all other user interface, so only the list and the icon "Closed Chains" are clickable, the user can reorder the event types, and either abort (clicked outside) aborts the reordering, or the click on "closed Chain" freezes the new reordering, after the metrictype array gets resorted from the dom order. testcase: add sample data, make screenshot of settings:eventtypes original order, press reorder, take screenshot, reorder third to first, fifth to second, take screenshot, press lock, screenshot.

- welltrack_lab: add function of a lab thats sole purpose is to analyze data gathered from welltrack.html. Icon to create from create-sample-data.py , icon to open/import from user, icon to download/save to user, make all data in json metrics, eventtypes, settings available, and editable.
    - automatic creation of timeslot sum for pain and mood values, bucket pain values, bucket mood values, make timebased average on switchable eventType,
    - make day to day mood/pain/eventtype comparison charts, day of week to day of week, whole 4 weeks to another 4 weeks with aligned dayofweek.
    - correlation study: chart to visualize how mood entry values of one mood question are correlated to another
    - make bar charts for group, pain, mood to display percentage of value of a group, of a mood, of a pain in the total.
    - make pushbutton entries overlayable to any chart (eg. take a medication)
    - use any modern tool availabel in the techstack (see `pyproject.toml`) but any pure python or python package supported by pyodide (for wasm support in the marimo welltrack lab) is ok.

- Gui Translation
    make translations that are inside welltrack.html and are selected automatically on browser agent preferences, and switchable in settings "Darstellung" "Sprache", "Default", "Deutsch", "English", defaulting to "default" which uses the browser preferred language, if available, or English if not available.


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
