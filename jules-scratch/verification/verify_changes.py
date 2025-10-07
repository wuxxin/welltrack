import json
import re
from playwright.sync_api import sync_playwright, Page, expect

def test_welltrack_refactoring(page: Page, event_types_data: list):
    # 1. Go to the app and test the "Rebirth Message"
    page.goto("https://localhost:8443/welltrack/welltrack.html", wait_until="load")
    page.evaluate("localStorage.clear()")
    page.reload()
    page.locator("#nav-settings").click()
    page.locator("button[data-tab='data']").click()
    page.locator("button[onclick='WellTrackApp.events.handleDeleteAllData()']").click()
    page.locator("#confirm-action-btn").click()

    rebirth_overlay = page.locator("#rebirth-overlay")
    expect(rebirth_overlay).to_be_visible(timeout=5000)
    expect(rebirth_overlay).to_have_text(re.compile("Alle Daten wurden gelöscht."))
    page.screenshot(path="jules-scratch/verification/01_rebirth_message.png")
    expect(rebirth_overlay).to_be_hidden(timeout=5000)

    # 2. Test the 5-to-5 Day Logic and Protokoll Refactor
    metrics_data = [
        # This entry is on Jan 2, 2024 at 4:59 AM, so it belongs to the WellTrack day of Jan 1
        {"metric": "event_coffee_cups_timestamp", "timestamp": 1704164340000, "labels": {"activity": "coffee_cups", "name": "Kaffee Tassen", "unitType": "", "groupType": "Ernährung"}, "value": 1},
        # Mood slot 1 for Jan 2 (WellTrack Day)
        {"metric": "mood_energy_level", "timestamp": 1704186000000, "labels": {"mood_id": "energy", "name": "Energie"}, "value": 2}, # 10:00
        {"metric": "mood_anxiety_level", "timestamp": 1704186060000, "labels": {"mood_id": "anxiety", "name": "Angstfreiheit"}, "value": 1}, # 10:01
        # Mood slot 2 for Jan 2 (WellTrack Day)
        {"metric": "mood_focus_level", "timestamp": 1704186900000, "labels": {"mood_id": "focus", "name": "Fokus"}, "value": 3} # 10:15
    ]

    page.evaluate(f"localStorage.setItem('wellTrackMetrics', '{json.dumps(metrics_data)}')")
    page.evaluate(f"localStorage.setItem('wellTrackEventTypes', '{json.dumps(event_types_data)}')")

    # Reload and navigate to the log
    page.reload()
    page.locator("#nav-log").click()

    # Use the app's own navigation to go to the first week with entries
    page.locator("#log-week-first").click()

    # Wait for the log entries to be rendered
    page.wait_for_selector("#log-entries-container > .py-4")

    # Verify WellTrack day of Jan 1, 2024
    day_of_jan_1 = page.locator("#log-day-1704081600000") # Timestamp for 2024-01-01 05:00:00
    expect(day_of_jan_1).to_be_visible()
    expect(day_of_jan_1.locator("text=Kaffee Tassen")).to_be_visible()

    # Verify mood slotting and sorting for Jan 2, 2024
    day_of_jan_2 = page.locator("#log-day-1704168000000") # Timestamp for 2024-01-02 05:00:00
    expect(day_of_jan_2).to_be_visible()

    # Verify first mood slot (10:00 / 10:01)
    slot_1000 = day_of_jan_2.locator("h5:has-text('Um 10:00')")
    expect(slot_1000).to_be_visible()
    expect(slot_1000).to_contain_text("Gesamt: +3")
    slot_1000_items_container = slot_1000.locator("..").locator(".grid")
    all_items_text = slot_1000_items_container.all_inner_texts()
    item_texts = all_items_text[0].split('\\n')
    expect(item_texts[0]).to_contain("Angstfreiheit")
    expect(item_texts[1]).to_contain("Energie")

    # Verify second mood slot (10:15)
    slot_1015 = day_of_jan_2.locator("h5:has-text('Um 10:15')")
    expect(slot_1015).to_be_visible()
    expect(slot_1015).to_contain_text("Gesamt: +3")
    expect(slot_1015.locator("..").locator(".grid")).to_contain_text("Fokus")

    page.screenshot(path="jules-scratch/verification/02_protokoll_refactor.png", full_page=True)

if __name__ == "__main__":
    with open("src/welltrack/welltrack.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    default_events_json_match = re.search(r"DEFAULT_EVENTS_JSON: `(.*?)`", html_content, re.DOTALL)
    if not default_events_json_match:
        raise ValueError("Could not find DEFAULT_EVENTS_JSON in the HTML file.")

    default_events_json_str = default_events_json_match.group(1).strip()
    event_types_data = json.loads(default_events_json_str)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        page = browser.new_page(ignore_https_errors=True)
        test_welltrack_refactoring(page, event_types_data)
        browser.close()