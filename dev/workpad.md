# WorkPad

## New Tasks

Read `dev/system-workflow.md`, `dev/product-requirements.md`, `dev/development.md`,  `README.md`, and `src/welltrack/welltrack.html`.
Read the following required changes, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update `dev/tasks.md` under Section "Planned Tasks" with the detailed description of that tasks.
Then, do each of the described tasks one by one, and update `dev/tasks.md` accordingly.
Request a user review once finished.

required changes:

make a some gui test cases. use pytest-playwright, add a new file in tests, make the test calling available as a step in Makefile: "make test" (currently existing but only creates the test import data. always test on a virtual screen size in portrait mode (mobile) of 1080 x 1920. use the build/tests/sample-data.json as Importfile in the pytest runner. load it once from file, write wellTrackMetrics wellTrackEventTypes wellTrackSettings from this import json, overwrite maybe some settings in wellTrackSettings and make test case. for every test case make a screenshot. name it clever so we can access it later on its name. write out the filenames of failed test screenshots.

initial tests:

- remove all wellTrack* localStorage, start welltrack, look for Today, "Heute" and Date
- do this with existing but all empty wellTrack*
- do this with the default data provided from sample-data.json , all further tests use default data
- click through all main bar icons, and check for the titel of the subtab


---

- refactor all console.log() calls next to location.reload(): save a rebirth_message settings to settings, then reload, on next init, check rebirth_message after loading settings from LocalStorage, and display overlay like Version Overlay, but in a way that versionoverlay and rebirth_message_overlay can be displayed simultan. make messagemodal color as version modal (blackish). make the modal layout linear: "icon Titel-in-Bold Message can overflow col", try to use screenwidth for width. if localstorage wellTrackSettings: hide_modal_overlays that will be loaded to state on init, is set (default is unset, can be only set by eg pywright directly to localstorage, but not by welltrack.html) do not display rebirth_overlay or version_overlay. This is for taking clean screenshots while testing.

- Alternating Styles (background, slightly) bei:Heute,Heutige Einträge,Protokoll: Day Card Entries,Settings:Edit EventTypes,EventType List.

- settings:edit eventtypes: keep edit icon and titel left,put rest (unit,groupicon,groupname) to the right next to delete.
also, dont display groupicon and groupname if group is none, but keep the three (unit groupicon,groupname) a flex group.


- feature: heute= 05-05
changes today page: bei pushbutton wie oft "X" , oder daily event value reset, bezieht sich auf 5 bis 5
ausserdem soll today bei 00->05:00: nicht nur "Heute -> Dienstag 3.10.2025" sondern "Heute -> Montag auf Dienstag 3.10.2025" anzeigen. Layout bleibt gleich, inhalt verändert sich. clear to 0 für daily values soll erst um 05:00 passieren. also true for the today page and the event entry page where  push button values should state "3x last 03:30" if three times during last day up to next day 03:30" in event entry, and should also undo to last day, because it is currently the "same" day.  also after 5 its 0 again and unpushed. this heute=05-05 does not change mood and pain trend on the today page: the mood and pain trends stay the same, because they are current againt previous value and are not day related. diagrams could change, but for now we ignore this. this also changes protokol, see feature protokol refactor, if easy doable without modifying programflow make the timeadjustment factor adjustable in settings: Darstellung/ Neuer Tag beginnt um: hh:mm. do a screenshot before after compare.

- feature protokol refactor: keep layout same, but current data gathering is not right. this needs to be rewritten for 05 to 05 anyways.
protokol gui stays same unless explicitly mentioned, one day card stays same unless explizit mentioned, but mood and pain groups and pushbutton events display get refactored,
Protokoll Week Selector Lin e ("Protokoll" and Weekselector Gui) will be fixed and not scroll with rest of page, so user can select week is always on top on protokoll subtab).
Display Protokoll day on the left side, left aligned, name it "Dienstag 7.10.2025 auf Mittwoch" to clarify the 05 to 05, make it also fixed so it doesnt scroll with day card entry, but changes to next date once day card is scrolled to another day.
Display Evententries Time (for all time displays in protokoll) instead of "Um hh:mm" as "<Icon: clock> <hh:mm>" if same day < 23:59, and "<Icon: clock-plus> <hh:mm> if time between 0 and 5am.

for mood values: from the first entry of that day (eg. 05:01 on Day and down to the last entry of day+1 04:59 ).
for each mood_* create a array entry (timestamp, mood_value_dict) and put this value all later values within 10 minutes in the value_dict with the first timestamp, do this until all mood of the day is processed. Then reverse the array, then rearrange into synced timestamp, serialized moodvalue_dict sorted by name of mood_entry for mood block.
for each pain_* create a array entry (timestamp, pain_value_dict) do the same like with mood,
for push button events that span over 00:00 should be displayed on the origin date card (the day before).
order of "Ereignisse" einträge: Order non time displayed entries first, then all other "ereignisse" events of that group (eg. pushbutton groups).
Group entries without group with wording "Allgemein" instead of "ohne gruppe".  do a screenshot before after compare.

---

- Alternating Styles (background, slightly) bei:Heute,Heutige Einträge,Protokoll: Day Card Entries,Settings:Edit EventTypes,EventType List.

- settings:edit eventtypes: keep edit icon and titel left,put rest (unit,groupicon,groupname) to the right next to delete.
also, dont display groupicon and groupname if group is none, but keep the three (unit groupicon,groupname) a flex group.


## nice to have



+ refactor: verlauf, mood and pain chart:
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
