# WorkPad

## New Tasks

Read `dev/system-workflow.md`, `dev/product-requirements.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.
Request a user review once finished.

required changes:

- create-sample-data.py:  at Generate Mood and Pain Data: check after assign of slots_for_today, if on last day and slot end_hour > currenttime: delete slot, random slot add, sort, recheck

- protokoll: remove log-day-indicator, instead put it as simple content before "Ereignisse" in the day card, and display as: "Mittwoch 8.10.2025 auf Donnerstag"

- Alternating Styles (background, slightly brightness variation, keep it similar but distinctable) for: Heute: Heutige Einträge and for  Settings:Edit EventTypes,EventType List.

- settings:edit eventtypes: keep edit icon and titel left,put rest "(value unit | pushbuttonicon) [groupicon groupname]" to the right next to delete.
also, if group is none, but keep the content parts a flex group.

- event entry: push button entry: Pressing "Erneut" or "rückgängig, Flashes the updated "(2x, zuletzt um hh:mm)" so user sees visual feedback on pressing erneut or rückgängig.

- on access using "file:///home/wuxxin/code/welltrack/src/welltrack/welltrack.html": Access to manifest at 'file:///home/wuxxin/code/welltrack/src/welltrack/manifest.json' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: chrome, chrome-extension, chrome-untrusted, data, http, https, isolated-app. If possible, make it work with file:/// to, or explain why this is not possible in settings: "Erinnerungen" on enable "Browser benachrichtigungen erlauben" function.

## nice to have

+ settings: edit event type: add Button (after subtab selector, right aligned just before event type list starts) with only an Icon (no text, but hovering reveals "Sortierung verändern", Representing "Loosing Chains" for reorder, and "closed Chains" as the other icon once in reorder mode to freeze changes. clicking "Reorder" Icon blurs everything except the event type list, that gets grab icons on the left, and disables/greysout (modal type) all other user interface, so only the list and the icon "Closed Chains" are clickable, the user can reorder the event types, and either abort (clicked outside) aborts the reordering, or the click on "closed Chain" freezes the new reordering, after the metrictype array gets resorted from the dom order.

+ body pain entry tab: body: new subselector (additional to back and front) other: other "Weitere" is a svg like front and back with "SchmerzFrei" as on the other svg's , but with selected bodyparts that are grouped for detailed not covered on front and back parts, eg: ears, eyes, nose, mouth, fingers , toes, and some special "pain" like "tinitus" seperated.

+ refactor: verlauf, mood and pain chart:
    + prepare chart data: for the timerange (plus mvag days added if data is available) selected go through all mood entrys
    + begin with the first entry, collect all mood data in 10 minute (from the first entry) in one group,
    then create 6 buckets and fill them according there mood value (-3,-2,-1,1,2,3),
    then create 6 buckets , -2, -1 , 1, 2, 3 sum of this bucket, and create a this then
    Total -3 , Ziemlich -2 , Ein Wenig -1
    verlauf: stimmung 1 is broken:
        + does not correctly count. uses either negativ or positiv, but not the value.
    verlauf: mood and pain chart: mavg of the totalsum (gesamtschmerz, gesamtwert stimmung) value

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
