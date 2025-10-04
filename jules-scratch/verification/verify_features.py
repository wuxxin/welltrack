import asyncio
from playwright.async_api import async_playwright, expect
import os
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('src/welltrack/welltrack.html')
        await page.goto(f'file://{file_path}')

        # --- 1. Clear Data and Setup ---
        await page.evaluate("() => localStorage.clear()")
        await page.reload()
        await page.wait_for_load_state('networkidle')

        # --- 2. Test "Nur Aufzeichnen" and Create Event Types ---
        settings_nav = page.locator("#nav-settings")
        await settings_nav.click()
        await expect(settings_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Einstellungen")).to_be_visible()

        await page.locator("button[data-tab='eventTypes']").click()

        # Create a "Record Only" event
        await page.locator("#add-new-event-btn").click()
        await expect(page.get_by_role("heading", name="Neue Ereignisart")).to_be_visible()
        await page.locator("#event-name").fill("Tagebucheintrag")
        await page.locator("#event-activity").fill("journal_entry")
        await page.locator("#event-group").fill("")
        await page.locator("#event-increment").fill("0")
        await page.locator("#event-display-type").select_option("3") # "Nur Aufzeichnen"
        await page.get_by_role("button", name="Speichern").click()

        # Create a standard event for comparison
        await page.locator("#add-new-event-btn").click()
        await expect(page.get_by_role("heading", name="Neue Ereignisart")).to_be_visible()
        await page.locator("#event-name").fill("Spaziergang")
        await page.locator("#event-activity").fill("walking")
        await page.locator("#event-increment").fill("15")
        await page.locator("#event-unit").fill("min")
        await page.locator("#event-group").fill("Bewegung")
        await page.locator("#event-display-type").select_option("1") # "Einzeln, hervorheben"
        await page.get_by_role("button", name="Speichern").click()

        # Wait for the list to update after the last save
        await expect(page.locator("#manage-event-list")).to_contain_text("Spaziergang")

        await page.screenshot(path="jules-scratch/verification/1_settings_nur_aufzeichnen.png")

        # --- 3. Test Event Type Reordering ---
        reorder_button = page.locator("#reorder-event-types-btn")
        await expect(reorder_button).to_be_enabled()
        await reorder_button.click()

        await expect(reorder_button).to_contain_text("Fertig")
        await page.screenshot(path="jules-scratch/verification/2_settings_reorder_mode.png")

        # The first created event is "Tagebucheintrag", the second is "Spaziergang"
        tagebuch_item = page.locator("#manage-event-list > div:nth-child(1)")
        spaziergang_item = page.locator("#manage-event-list > div:nth-child(2)")

        # Drag 'Spaziergang' (item 2) to the position of 'Tagebucheintrag' (item 1)
        await spaziergang_item.drag_to(tagebuch_item)

        await page.screenshot(path="jules-scratch/verification/3_settings_reordered.png")
        await reorder_button.click() # Save the new order

        # Verify order is saved after reload
        await page.reload()
        await page.wait_for_load_state('networkidle')
        await settings_nav.click()
        await expect(settings_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Einstellungen")).to_be_visible()
        await page.locator("button[data-tab='eventTypes']").click()

        first_item = page.locator("#manage-event-list > div:nth-child(1)")
        await expect(first_item).to_contain_text("Spaziergang")
        await page.screenshot(path="jules-scratch/verification/4_settings_reorder_saved.png")

        # --- 4. Test Log Sorting & "Nur Aufzeichnen" Visibility ---

        # Add mood entry (oldest)
        mood_nav = page.locator("#nav-mood")
        await mood_nav.click()
        await expect(mood_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Stimmung")).to_be_visible()
        await page.locator(".mood-slider-wrapper").first.click(position={'x': 20, 'y': 20})
        await asyncio.sleep(0.2)

        # Add event entries
        event_nav = page.locator("#nav-event")
        await event_nav.click()
        await expect(event_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Ereignisse")).to_be_visible()

        # Add 15 min Spaziergang (in "Bewegung" group, active by default)
        await page.locator("#event-item-walking button").last.click()
        await asyncio.sleep(0.2)

        # Switch to "Ohne Gruppe" to log the other event
        await page.get_by_role("button", name="Ohne Gruppe").click()
        await expect(page.locator("#event-item-journal_entry")).to_be_visible()

        # Add Tagebucheintrag
        await page.locator("#event-item-journal_entry button").click()
        await asyncio.sleep(0.2)

        # Add a pain entry (newest)
        pain_nav = page.locator("#nav-pain")
        await pain_nav.click()
        await expect(pain_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Schmerzen")).to_be_visible()
        await page.locator("#back_lower_back_middle").click()
        await expect(page.get_by_role("heading", name=re.compile("Schmerz .*"))).to_be_visible()
        await page.get_by_role("button", name="S (Stark)").click()

        # --- 5. Verify Pages ---
        # Verify Today page
        today_nav = page.locator("#nav-today")
        await today_nav.click()
        await expect(today_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Heute")).to_be_visible()
        await expect(page.get_by_text("Spaziergang")).to_be_visible()
        await expect(page.get_by_text("Tagebucheintrag")).to_be_hidden()
        await page.screenshot(path="jules-scratch/verification/5_today_page.png", full_page=True)

        # Verify History page
        history_nav = page.locator("#nav-history")
        await history_nav.click()
        await expect(history_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Verlauf")).to_be_visible()
        await expect(page.get_by_text("Tagebucheintrag")).to_be_hidden()
        await page.screenshot(path="jules-scratch/verification/6_history_page.png", full_page=True)

        # Verify Log page
        log_nav = page.locator("#nav-log")
        await log_nav.click()
        await expect(log_nav).to_have_class(re.compile(r'\bactive\b'))
        await expect(page.get_by_role("heading", name="Protokoll")).to_be_visible()
        await page.screenshot(path="jules-scratch/verification/7_log_page.png", full_page=True)

        # Verify the order in the log
        log_entries_container = page.locator("#log-entries-container")
        await expect(log_entries_container.locator("> div").first).to_be_visible() # Wait for entries to render
        log_entries_text = await log_entries_container.inner_text()

        pain_pos = log_entries_text.find("Schmerz um")
        event_pos = log_entries_text.find("Ereignis Tagebucheintrag")
        mood_pos = log_entries_text.find("Stimmung um")

        assert pain_pos != -1 and event_pos != -1 and mood_pos != -1, "Not all log entry types were found"
        assert pain_pos < event_pos < mood_pos, f"Log entries are not sorted correctly. Pain: {pain_pos}, Event: {event_pos}, Mood: {mood_pos}"

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())