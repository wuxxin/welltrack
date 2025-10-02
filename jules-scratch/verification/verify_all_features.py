
import json
import time
from playwright.sync_api import sync_playwright, Page, expect
import os

def setup_data_for_pain_trend(page: Page):
    now = int(time.time() * 1000)
    ten_minutes_ago = now - (10 * 60 * 1000)
    twenty_one_minutes_ago = now - (21 * 60 * 1000)

    pain_metrics = [
        {
            "metric": "pain_back_head_level",
            "timestamp": twenty_one_minutes_ago,
            "labels": {"body_part": "back_head", "name": "Hinterkopf"},
            "value": 2
        },
        {
            "metric": "pain_back_head_level",
            "timestamp": ten_minutes_ago,
            "labels": {"body_part": "back_head", "name": "Hinterkopf"},
            "value": 4
        }
    ]
    page.evaluate(f"localStorage.setItem('wellTrackMetrics', '{json.dumps(pain_metrics)}')")

def setup_data_for_pagination(page: Page):
    metrics = []
    for i in range(15):
        timestamp = int((time.time() - (i * 24 * 3600)) * 1000)
        metrics.append({
            "metric": "event_walking_value",
            "timestamp": timestamp,
            "labels": {"activity": "walking", "name": "Spaziergang", "unitType": "min", "groupType": "Bewegung"},
            "value": 30 + i
        })
    page.evaluate(f"localStorage.setItem('wellTrackMetrics', '{json.dumps(metrics)}')")


def run_verification(page: Page):
    # Get the absolute path to the HTML file
    file_path = os.path.abspath('src/welltrack/welltrack.html')

    # Go to the local HTML file
    page.goto(f'file://{file_path}')
    page.wait_for_load_state('networkidle')

    # 1. Verify "Letzte Einträge" is a collapsible button
    # Add some data to make the button appear
    page.evaluate("localStorage.setItem('wellTrackMetrics', JSON.stringify([{'metric': 'mood_energy_level', 'timestamp': Date.now(), 'labels': {'mood_id': 'energy', 'name': 'Energie'}, 'value': 1}]))")
    page.reload()
    page.wait_for_load_state('networkidle')

    letzte_eintrage_button = page.locator('button:has-text("1 heutige Einträge")')
    expect(letzte_eintrage_button).to_be_visible()
    page.screenshot(path="jules-scratch/verification/01_letzte_eintrage_collapsed.png")

    letzte_eintrage_button.click()
    expect(page.locator('#todays-log-container')).not_to_have_class('hidden')
    page.screenshot(path="jules-scratch/verification/02_letzte_eintrage_expanded.png")

    # 2. Verify Settings sub-tabs
    page.get_by_title("Einstellungen").click()
    expect(page.locator("h2:has-text('Einstellungen')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/03_settings_subtabs.png")

    # 3. Verify sub-tab alignments
    page.get_by_title("Verlauf").click()
    expect(page.locator("h2:has-text('Verlauf')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/04_verlauf_alignment.png")

    page.get_by_title("Schmerzen eintragen").click()
    expect(page.locator("h2:has-text('Schmerzen')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/05_schmerzen_alignment.png")

    page.get_by_title("Stimmung eintragen").click()
    expect(page.locator("h2:has-text('Stimmung')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/06_stimmung_alignment.png")

    # 4. Verify Pain Trend
    setup_data_for_pain_trend(page)
    page.locator("#nav-today").click()
    expect(page.locator("p:has-text('Schmerzen')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/07_pain_trend.png")

    # 5. Verify Protokoll Pagination
    setup_data_for_pagination(page)
    page.get_by_title("Protokoll").click()
    expect(page.locator("h2:has-text('Protokoll')")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/08_protokoll_pagination_styled.png", full_page=True)

    page.get_by_role("button", name="Weiter").click()
    # Give it a moment for the smooth scroll to finish
    page.wait_for_timeout(500)
    page.screenshot(path="jules-scratch/verification/09_protokoll_pagination_scrolled.png")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        run_verification(page)
        browser.close()

if __name__ == "__main__":
    main()
