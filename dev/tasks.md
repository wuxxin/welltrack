# Tasks

This document lists the curren implementation status of features and refactorings for the WellTrack health diary app.

## Planned Tasks

- [x] **make a new prototype in `src/prototype/new-pain-entry.html`**: create a skeleton welltrack gui mainbar, tailwind css, mimicking the welltrack app but only the body pain part interface is exposed. a click on the home icon reveals a list of currently created metric with time and metricname value to verify working entry logic. refaktor out the body svg's and selection. it should be able to select body parts, select the pain level, and highlight the already set body_parts in the color of the pain level, and record the pain entries to an array equal to welltrack.
- [x] **the pain entry chart resets (as welltrack) afer 10min and resets all body part input to zero (including pain_frree) for the display, but the metrics are kept.**
- [x] **within a 10 minute period (as welltrack) it is possible to change body part entries, by assigning them a new value. the old value is looked up, deleted, and a new value is added on top of the metrics, like in welltrack.**
- [x] **pain entry back svg: split "LWS" vertically, upper part remains LWS, lower part becomes "KSB" with long german text "Kreuz & Steißbein", remove pain_free.**
- [x] **pain entry front svg: split "brust" und "bauch" to left and right part. remove pain_free.**
- [x] **new subselector: other named "Weitere". A list in two cols, of user created special pain entry possibilities, but the first item on the list is alway the new "pain free" item. use the `src/prototype/pain-free-selector.html` "Body Icon" for "{BodyIcon} Schmerz Frei" as title of first item.  make the icon and the title appear as one line, the icon about the size of the title font.**
- [x] **other items are generated from the list of extra painTypes a new array similar to eventTypes, but for custom pain entries: eg. '{"pain_id": "english_clear_name", name="German Common Name", icon="material-icon-name"}'. for this demo assume two custom Entries, "Tinitus" and "Sodbrennen", give tinitus title a fitting icon in the title, equal for sodbrennen, so its displayed "icon titlename" . if pressed they behave like other body pain parts, they become filled with the pain value color, and a welltrack metric is generated.**
- [x] **on init, any body/pain part that should be colored, look metrics latest to earlier within the last 10 minutes for pain entries add each color value found with the level. if any pain_free_level or 10 min is encountered further processing is stopped.**
- [x] **if any pain that is clicked, it looks within the last 10 minutes (latest to earlier) of pain entries if there is a pain_free_level or another pain_bodypart metric of the same type that would be replaced with the new value, then delete the old entry (pain_free_level, or the old pain_bodypart metric), attach a new entry with the new pain metric.**
- [x] **if "pain free" button is selected, it looks if there are set pain parts in the last 10 minutes, and if so it asks with a modal, "wieder Schmerzfrei ?" "Nein" und "Ja", if "ja" it goes back 10 minutes, and removes all pain entries from their to now. it then adds the pain_free metric, and colors the button if there was no question or the question was answered with ja.**
- [x] **create a settings "Schmerzarten" submenu, that allows creating, editing and deleting special pain entries, like EventTypes Edit. In addition to the button "hinzufügen", there is "Sortierung verändern", with an icon representing "Loosing Chains" for reorder, and "closed Chains" as the other icon once in reorder mode to freeze changes. clicking "Reorder" Icon blurs everything except the event type list, that gets grab icons on the left, and disables/greysout (modal type) all other user interface, so only the list and the icon "Closed Chains" are clickable, the user can reorder the event types, and either abort (clicked outside) aborts the reordering, or the click on "closed Chain" freezes the new reordering, after the paintype array gets resorted from the dom order and saved.**
- [x] **create a test in tests that uses this prototype as file url open f"file://{basedir}/src/prototype/new-pain-entry.html" and take screenshots from painentry: back, front and other tab to mkdir `build/tests/new-pain-entry/`.**
- [x] **then copy those screenshots using `mkdir jules-scratch/verify; cp build/tests/new-pain-entry/* jules-scratch/verify`.**
- [x] **then verify those screenshots.**

## Completed Tasks

- [x] **Refactor Submenu Layouts**: Update the submenu layout on the Event, Mood, Pain, History, and Settings tabs. The title will be on its own line, and the submenu will be on the next line, right-aligned, with items flowing from right to left and wrapping downwards.
- [x] **Refactor Log Page Layout**: Adjust the log/protocol page so the title and protocol selector form a fixed unit attached to the header bar, preventing them from moving with the content.
- [x] **Refactor PushButton Event Layout**: In the Event Entry tab, modify the "PushButton" layout to ensure the title (e.g., "Titel [(4x, zuletzt um hh:mm)]") is on one line and the action buttons ("Einnahme", "Rückgängig", "Erneute Einnahme") are on a second, right-aligned line. This will create a stable UI that does not change size based on the button state.
- [x] **Fix GUI Flicker**: Resolve the layout flicker on event entry pushbuttons.
- [x] **Restyle Pushbutton Event Info**: Align the timestamp text to the right, remove parentheses, and make it semibold.

## Discovered Tasks
