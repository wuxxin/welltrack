import os
import re
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    # Setup
    browser = playwright.chromium.launch(headless=True)
    # Use a smaller mobile viewport to better test wrapping and responsiveness
    context = browser.new_context(viewport={"width": 375, "height": 812}) # iPhone X
    page = context.new_page()

    # Get absolute path for the local HTML file
    file_path = os.path.abspath('src/welltrack/welltrack.html')
    page.goto(f'file://{file_path}')

    # 1. Today Page Screenshot
    print("Capturing Today page...")
    page.wait_for_selector('#today-summary-cards')
    page.screenshot(path="jules-scratch/verification/01_today_page.png", full_page=True)

    # 2. Ereignisse (Events) Tab Screenshot
    print("Capturing Ereignisse tab...")
    page.get_by_title("Ereignis eintragen").click()
    page.wait_for_selector('#todays-event-container')

    # Inject more event groups to test wrapping
    page.evaluate("""() => {
        let events = WellTrackApp.data.getEvents();
        const newGroups = ['Bewegung', 'Ernährung', 'Medikamente', 'Mentales', 'Soziales', 'Arbeit', 'Haushalt', 'Sonstiges'];
        // Clear existing events to ensure a clean slate for the test
        WellTrackApp.data.saveEvents([]);
        events = [];
        newGroups.forEach((group, index) => {
            events.push({
                "name": `Test ${index}`, "activity": `test_${index}`, "displayType": 0,
                "increment": 1, "unitType": "x", "groupType": group
            });
        });
        WellTrackApp.data.saveEvents(events);
        WellTrackApp.state.activeEventGroup = 'Bewegung'; // Set a default active group
        WellTrackApp.render.eventPage();
    }""")
    page.screenshot(path="jules-scratch/verification/02_ereignisse_tab_wrapping.png", full_page=True)

    # 3. Stimmung (Mood) Tab Screenshot
    print("Capturing Stimmung tab...")
    page.get_by_title("Stimmung eintragen").click()
    page.wait_for_selector('#mood-container')
    page.screenshot(path="jules-scratch/verification/03_stimmung_tab.png", full_page=True)

    # 4. Schmerzen (Pain) Tab Screenshot
    print("Capturing Schmerzen tab...")
    page.get_by_title("Schmerzen eintragen").click()
    page.wait_for_selector('#pain-section-title')
    page.screenshot(path="jules-scratch/verification/04_schmerzen_tab.png", full_page=True)

    # 5. Verlauf (History) Tab Screenshot
    print("Capturing Verlauf tab...")
    page.get_by_title("Verlauf").click()
    page.wait_for_selector('#chart-container-event')
    page.screenshot(path="jules-scratch/verification/05_verlauf_tab.png", full_page=True)

    # 6. Protokoll (Log) Tab Screenshot
    print("Capturing Protokoll tab...")
    page.get_by_title("Protokoll").click()
    page.wait_for_selector('#log-pagination')
    page.screenshot(path="jules-scratch/verification/06_protokoll_tab.png", full_page=True)

    # 7. Settings - Delete Event Modal Screenshot
    print("Capturing Settings - Delete Modal...")
    page.get_by_title("Einstellungen").click()
    page.wait_for_selector('#settings-tab-eventTypes')
    page.get_by_role("button", name="Ereignisarten").click()
    # Click first delete button on one of our test events
    page.locator('button[onclick*="handleRemoveEvent"]').first.click()
    expect(page.locator('#modal-container')).to_be_visible()
    page.screenshot(path="jules-scratch/verification/07_settings_delete_modal.png")
    # Close modal
    page.get_by_role("button", name="Abbrechen").click()
    expect(page.locator('#modal-container')).to_be_hidden() # Ensure modal is gone

    # 8. Settings - Edit Event Form Scroll Screenshot
    print("Capturing Settings - Edit Form scroll...")
    page.get_by_role("button", name=re.compile("Neue hinzufügen")).click()
    page.wait_for_timeout(1000) # wait for scroll animation
    page.screenshot(path="jules-scratch/verification/08_settings_edit_event_form_scrolled.png", full_page=True)
    page.get_by_role("button", name="Abbrechen").click()

    # 9. Settings - Data Import Modal Screenshot
    print("Capturing Settings - Import Modal...")
    page.get_by_role("button", name="Datenverwaltung").click()

    # Create a dummy file for upload
    dummy_path = "jules-scratch/verification/dummy_data.json"
    with open(dummy_path, "w") as f:
        f.write('{"metrics":[],"events":[],"settings":{}}')

    # Set input for file chooser
    with page.expect_file_chooser() as fc_info:
        # The input is visually hidden but the label is not
        page.locator('label:has-text("Daten importieren")').click()
    file_chooser = fc_info.value
    file_chooser.set_files(dummy_path)

    expect(page.locator('#modal-container')).to_be_visible()
    page.screenshot(path="jules-scratch/verification/09_settings_import_modal.png")
    page.get_by_role("button", name="Abbrechen").click()
    expect(page.locator('#modal-container')).to_be_hidden()


    # Cleanup
    print("Verification script finished.")
    browser.close()

with sync_playwright() as p:
    run(p)