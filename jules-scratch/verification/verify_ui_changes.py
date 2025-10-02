import os
import json
import time
import re
from playwright.sync_api import sync_playwright, Page, expect

def setup_data(page: Page, metrics: list, events: list = None):
    """Injects metrics and events data into localStorage."""
    page.evaluate(f"localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(metrics)}));")
    if events:
        page.evaluate(f"localStorage.setItem('wellTrackEvents', JSON.stringify({json.dumps(events)}));")

    # Also clear other relevant storage to ensure a clean state for the test
    page.evaluate("localStorage.removeItem('wellTrackLogVisibility');")
    page.evaluate("localStorage.removeItem('wellTrackActiveSettingsTab');")
    page.reload()
    # Short wait to ensure DOM is updated after reload
    page.wait_for_timeout(100)


def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 1024})
    page = context.new_page()

    base_path = os.path.abspath("src/welltrack/welltrack.html")
    page.goto(f"file://{base_path}")

    # --- 1. Verify Sub-tab alignment (Stimmung, Schmerzen, Verlauf) ---
    print("Verifying sub-tab alignments...")
    page.locator("#nav-mood").click()
    expect(page.get_by_role("heading", name="Stimmung")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/mood_tab_alignment.png")

    page.locator("#nav-pain").click()
    expect(page.get_by_role("heading", name="Schmerzen")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/pain_tab_alignment.png")

    page.locator("#nav-history").click()
    expect(page.get_by_role("heading", name="Verlauf")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/history_tab_alignment.png")

    # --- 2. Verify Settings Sub-tabs ---
    print("Verifying settings sub-tabs...")
    page.locator("#nav-settings").click()
    expect(page.get_by_role("heading", name="Einstellungen")).to_be_visible()

    # Check default active tab
    expect(page.locator(".settings-tab[data-tab='eventTypes']")).to_have_class(re.compile(r"\bactive\b"))
    expect(page.locator("#settings-tab-eventTypes")).to_be_visible()
    expect(page.locator("#settings-tab-data")).not_to_be_visible()
    page.screenshot(path="jules-scratch/verification/settings_default_tab.png")

    # Click another tab and verify
    page.locator(".settings-tab[data-tab='data']").click()
    expect(page.locator(".settings-tab[data-tab='data']")).to_have_class(re.compile(r"\bactive\b"))
    expect(page.locator("#settings-tab-data")).to_be_visible()
    expect(page.locator("#settings-tab-eventTypes")).not_to_be_visible()

    # Verify persistence on reload
    page.reload()
    page.wait_for_timeout(100)
    page.locator("#nav-settings").click()
    expect(page.get_by_role("heading", name="Einstellungen")).to_be_visible()
    expect(page.locator(".settings-tab[data-tab='data']")).to_have_class(re.compile(r"\bactive\b"))
    expect(page.locator("#settings-tab-data")).to_be_visible()

    # --- 3. Verify Collapsible Log and Pain Trend on Today page ---
    print("Verifying 'Today' page changes...")
    now = int(time.time() * 1000)

    # Setup data for both pain increase and log visibility
    pain_increase_metrics = [
        {"metric": "pain_back_head_level", "timestamp": now - 700000, "labels": {"body_part": "back_head", "name": "Hinterkopf"}, "value": 1},
        {"metric": "pain_back_head_level", "timestamp": now, "labels": {"body_part": "back_head", "name": "Hinterkopf"}, "value": 3}
    ]
    setup_data(page, pain_increase_metrics)
    page.locator("#nav-today").click()
    expect(page.get_by_role("heading", name="Heute")).to_be_visible()

    # Verify log is hidden by default
    expect(page.locator("#todays-log-container")).to_be_hidden()

    # Verify pain trend UP (bad)
    pain_pill_delta_up = page.locator(".pill-card", has_text="Schmerzen").locator(".text-red-500")
    expect(pain_pill_delta_up).to_be_visible()
    expect(pain_pill_delta_up.locator(".material-symbols-outlined")).to_have_text("trending_up")
    page.screenshot(path="jules-scratch/verification/today_log_hidden_pain_up.png")

    # Click to show log
    page.get_by_role("button", name="Letzte Einträge").click()
    expect(page.locator("#todays-log-container")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/today_log_visible.png")

    # Setup data for pain decrease
    pain_decrease_metrics = [
        {"metric": "pain_back_head_level", "timestamp": now - 700000, "labels": {"body_part": "back_head", "name": "Hinterkopf"}, "value": 4},
        {"metric": "pain_back_head_level", "timestamp": now, "labels": {"body_part": "back_head", "name": "Hinterkopf"}, "value": 2}
    ]
    setup_data(page, pain_decrease_metrics)
    page.locator("#nav-today").click()
    expect(page.get_by_role("heading", name="Heute")).to_be_visible()

    # Verify pain trend DOWN (good)
    pain_pill_delta_down = page.locator(".pill-card", has_text="Schmerzen").locator(".text-green-500")
    expect(pain_pill_delta_down).to_be_visible()
    expect(pain_pill_delta_down.locator(".material-symbols-outlined")).to_have_text("trending_down")
    page.screenshot(path="jules-scratch/verification/pain_trend_down.png")

    # --- 4. Verify Protokoll Pagination ---
    print("Verifying 'Protokoll' pagination...")
    many_metrics = []
    for i in range(15):
        day_timestamp = now - (i * 24 * 60 * 60 * 1000)
        many_metrics.append({"metric": "mood_energy_level", "timestamp": day_timestamp, "labels": {"mood_id": "energy", "name": "Energie"}, "value": i % 3 + 1})
    setup_data(page, many_metrics)

    page.locator("#nav-log").click()
    expect(page.get_by_role("heading", name="Protokoll")).to_be_visible()

    # Check button style
    weiter_button = page.get_by_role("button", name="Weiter")
    expect(weiter_button).to_have_class(re.compile(r"btn-secondary"))
    page.screenshot(path="jules-scratch/verification/protokoll_pagination_style.png")

    # Check scroll behavior
    initial_scroll_y = page.evaluate("() => window.scrollY")
    weiter_button.click()
    page.wait_for_timeout(500)
    final_scroll_y = page.evaluate("() => window.scrollY")
    assert final_scroll_y > initial_scroll_y, f"Page did not scroll down. Start: {initial_scroll_y}, End: {final_scroll_y}"

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
print("Verification script finished successfully.")