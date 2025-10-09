import json
import re
import time
from pathlib import Path
from playwright.sync_api import Page, expect

def test_mood_chart_screenshots(page: Page, live_server):
    """
    Loads mood chart data and takes screenshots for different time ranges.
    """
    base_url = live_server
    page.goto(f"{base_url}/welltrack/welltrack.html")

    # Load the sample data
    sample_data_path = Path(__file__).parent.parent / "build/tests/mood-chart-data.json"
    with open(sample_data_path, "r") as f:
        sample_data = json.load(f)

    page.evaluate(f"localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])}))")
    page.evaluate(f"localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])}))")
    page.evaluate(f"localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])}))")

    # Navigate to history page
    page.get_by_title("Verlauf").click()

    # Wait for the history page to load and click the mood tab
    expect(page.get_by_role("heading", name="Verlauf")).to_be_visible()
    page.get_by_role("button", name="Stimmung").click()

    # Ensure chart container is visible
    chart_container = page.locator("#chart-container-mood")
    expect(chart_container).not_to_have_class(re.compile(r'hidden'))

    # --- Take screenshots for each time range ---
    output_dir = Path(__file__).parent.parent / "build/tests/output"
    output_dir.mkdir(exist_ok=True)

    # 7 Days
    page.locator("#time-range-selector").select_option("7")
    time.sleep(1) # Wait for chart animation
    page.screenshot(path=str(output_dir / "mood_chart_7_days.png"))

    # 4 Weeks
    page.locator("#time-range-selector").select_option("28")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "mood_chart_4_weeks.png"))

    # 3 Months
    page.locator("#time-range-selector").select_option("84")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "mood_chart_3_months.png"))

    print("\nScreenshots saved to build/tests/output/")
    print(" - mood_chart_7_days.png")
    print(" - mood_chart_4_weeks.png")
    print(" - mood_chart_3_months.png")