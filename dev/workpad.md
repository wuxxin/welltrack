
## New Tasks

Read system-workflow.md, product-requirements.md, README.md, and welltrack.html.
Read the following requirements, considering which parts of the tasks should be combined and which should be separate, and in what order they should be performed.
Update tasks.md under Section "Planned Tasks" with the detailed description of that tasks.
Do each of the described tasks one by one, and update tasks.md accordingly.
request the user review once finished.

required changes:


Tabs: Event Entry, Mood Entry, PainEntry, Verlauf,Protokoll and Settings:The Titel of the tab "Ereignisse", "Stimmung", "Schmerzen", "Verlauf", "Protokoll" should all have the same size as Stimmung or Schmerzen has, if it is on small screen (its less big, and this less big size should become the only size for this kind of heading). this also includes the settings sub header like "Ereignisarten" , "Datenverwaltung", "Erinnerungen", "Über diese WebApp". Make the sub headings in protokoll fitting relative in size of the main titel "Protokoll".

showConfirmation: make show confirmation take abort and confirm text prompts.

settings: delete event type, confirmation modal: abort="Abbrechen", confirm="Löschen"

settings: delete all data, confirmation modal: abort="Abbrechen", confirm="Löschen"

settings: delete event type: on click, check if eventtype is used in eventsarray anywhere, show error if it is used, claiming "Ereignissart kann nicht gelöscht werden, da es bereits Einträge dieser Art gibt."

body pain entry: back and frontside: add a circle like head but half size, and right of head at upper right corner of svg  with text in circle stating "Schmerz Frei" and if you click there, it will light up in light green (similar to the light blue of pain 1), all current (last 10min) of pain_*  will be cleared, and an entry pain_free_level value 0 with current timestamp will be set. as soon its clicked again, or any other pain entry is done, the pain_free_level will be deleted (if withhin 10min window), and  a new pain entry is done.
this way, we can record no pain "0" and make it different to no pain recorded, because the chart will take the pain_free_level with value 0 as entry, instead of no entry.

verlauf: mood and pain chart: remove mavg
verlauf: mood and pain chart: bars are only big on small number of entries, and become very thin even if only 7 events are shown. make the bars wider so they cover roughly the area between events.


## nice to have

is not from the right value, right value is the mavg of the totalsum (gesamtschmerz, gesamtwert stimmung) value

verlauf mood and pain: also on both: should not be bar type for negativ positiv, and pain body parts, but stacked area, and total and mavg should be colored and drawed distintivly over the area

make an additional dark theme, add switch to settings after Erinnerungen, "Darstellung", "Design", "Hell | Dunkel" , default hell

make icon bar switchable between up and down location, add switch to settings, after "Erinnerungen", "Darstellung" , "Menübalken" "Oben" | "Unten", default "Oben"

make browser forward and browser back work as go through recorded selected subtabs, eg. clicked on today, mood, go to mood entry, click browser back, return to today.

make translations that are inside welltrack.html and are selected automatically on browser agent preferences, and switchable in settings "Darstellung" "Sprache", "Default", "Deutsch", "English", defaulting to "default" which uses the browser preferred language, if available, or English if not available.

mood: gedankenschleifen , wenn immer neue da bin ich zb. das opfer gewesen, oder da war jemand asozial, und ich habe mich darüber geärgert, versuche ein gegensatz paar zu finden
