# WorkPad

## New Tasks

Read `dev/system-workflow.md`, `dev/product-requirements.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.
Request a user review once finished.

required changes:

- settings: edit event type: Anzeige-Art: Add posibility: "Nur Aufzeichnen" as last of the possibilities, so: "Zusammenzählen, Einzeln Hervorheben, Einzeln, Nur Aufzeichnen". settings that are "nur aufzeichen" have no distinct today and no verlauf diagram entry.

- protokoll: sort the entries of one day on newest first (pushbuttons, other timestamped, mood, pain), also remove any usage of `ENTRIES_PER_PAGE` , because we select the entries per week now.

- on reload and refresh, check the modified datetime of the welltrack.html as we refresh, if `settings:welltrack_latest` is older display short overlay showing the welltrack icon and "aktualisiert auf die Version 23.4.2025 23:25" and writes the version to `settings:welltrack_latest`. in `settings:about` it also shows the `welltrack_latest` version.

- settings: event type edit: make it a modal overlay that fits the viewport horizontally. the modal content is equal to the current edit content, a click out of the modal aborts, "abbrechen" aborts too.

- settings: edit event type: add Button (after subtab selector, right aligned just before event type list starts) with Icon Representing "Loosing Chains" for reorder, and "closed Chains" as the other icon once in reorder mode to freeze changes. clicking "Reorder" Icon blurs everything except the event type list, that gets grab icons on the left, and disables/greysout (modal type) all other user interface, so only the list and the icon "Closed Chains" are clickable, the user can reorder the event types, and either abort (clicked outside) aborts the reordering, or the click on "closed Chain" freezes the new reordering, after the metrictype array gets resorted from the dom order.


## nice to have


- refactor: `getEvents()` , `const events`, 'wellTrackEvents' including settings, and all mentions are all targeting the array of event types. Rename it everywhere to relect that this array purpose and the corresponding names and functionnames to reflect this naming. The Array is a `wellTackEventTypes` `EventTypes` , so its `getEventTypes`, `wellTrackEventTypes`, and so on.
- refactor code: `localStorage`: Only Write three items: `wellTrackSettings`, `wellTrackEventTypes`, `wellTrackMetrics`, migrate other into Settings.
- refactor code: load and write all states into settings that have an corresponding value there of have been saved to localstorage otherwise. reinitialize on page reload, refresh from settings item to state.


button next too mood: Record Note: TinyWhisper modul pushbutton while speaking , transcribe to text as note with mood entry
push button

push button gps coordinates event: event_location_present value=1 labels: geouri:12.3,14.4, is either automatic on body or pain entry if settings: location on Mood or Pain entry Yes, or under "*" in Events, "Standort erfassen", or on "*" events as "Standort erfassen"

refactor: verlauf, mood and pain chart:
+ prepare chart data: for the timerange (plus mvag days added if data is available) selected go through all mood entrys
+ begin with the first entry, collect all mood data in 10 minute (from the first entry) in one group,
then create 6 buckets and fill them according there mood value (-3,-2,-1,1,2,3),
 then create 6 buckets , -2, -1 , 1, 2, 3 sum of this bucket, and create a this then
Total -3 , Ziemlich -2 , Ein Wenig -1
verlauf: stimmung 1 is broken:
    + does not correctly count. uses either negativ or positiv, but not the value.
verlauf: mood and pain chart: mavg of the totalsum (gesamtschmerz, gesamtwert stimmung) value


+ body pain: body: back, front, other: other is a svg like front and back with "SchmerzFrei" as on the other svg's , but with selected bodyparts
  for detailed not covered on front and back parts, eg: ears, eyes, nose, mouth, fingers , toes, and some special "pain" like "tinitus" seperated.


+ Gui Dark Theme
    +make an additional dark theme, add switch to settings after Erinnerungen, "Darstellung", "Design", "Hell | Dunkel" , default hell

+ Gui Icon-Bar Placement
    make icon bar switchable between up and down location, add switch to settings, after "Erinnerungen", "Darstellung" , "Menübalken" "Oben" | "Unten", default "Oben"

+ Gui browser Forward/Back Utilization
    make browser forward and browser back work as go through recorded selected subtabs, eg. clicked on today, mood, go to mood entry, click browser back, return to today.

+ Gui Translation
    make translations that are inside welltrack.html and are selected automatically on browser agent preferences, and switchable in settings "Darstellung" "Sprache", "Default", "Deutsch", "English", defaulting to "default" which uses the browser preferred language, if available, or English if not available.


npx @google/jules


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
