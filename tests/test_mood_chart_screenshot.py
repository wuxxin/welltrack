import pytest
from playwright.sync_api import Page, expect
import json
import time


def test_mood_chart_screenshots(page: Page, live_server):
    """Takes screenshots of the mood chart for different time ranges.

    This test loads sample data, navigates to the history page, selects the
    mood chart, and then captures a full-page screenshot for each available
    time range (7, 28, and 84 days). This is useful for visual regression
    testing and documentation.

    Args:
        page (Page): The Playwright Page object.
        live_server (str): The base URL of the live server.
    """
    # Use a larger sample data file for better chart visualization
    with open("build/tests/sample-data.json", "r") as f:
        sample_data = json.load(f)

    # Use a script to import data via localStorage
    page.goto(f"{live_server}/welltrack/welltrack.html")
    page.evaluate(
        f"localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])}))"
    )
    page.evaluate(
        f"localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])}))"
    )
    page.evaluate(
        f"localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])}))"
    )

    # Reload the page to apply the data
    page.reload()

    # Navigate to the history page
    page.locator("#nav-history").click()

    # Click on the mood tab
    page.locator("button[data-tab='mood']").click()

    # Ensure the chart container is visible
    mood_chart_container = page.locator("#chart-container-mood")
    expect(mood_chart_container).not_to_be_hidden()

    # Allow time for chart animation
    time.sleep(1)

    # Take screenshot for 7 days view
    page.locator("#time-range-selector").select_option("7")
    time.sleep(1)  # wait for re-render
    page.screenshot(path="build/tests/output/mood_chart_7_days.png", full_page=True)

    # Take screenshot for 28 days view
    page.locator("#time-range-selector").select_option("28")
    time.sleep(1)  # wait for re-render
    page.screenshot(path="build/tests/output/mood_chart_28_days.png", full_page=True)

    # Take screenshot for 84 days view
    page.locator("#time-range-selector").select_option("84")
    time.sleep(1)  # wait for re-render
    page.screenshot(path="build/tests/output/mood_chart_84_days.png", full_page=True)
