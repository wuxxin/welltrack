import pytest
from playwright.sync_api import Page, expect
import os
import json
import time

def make_screenshot(page: Page, path: str):
    page.screenshot(path=path, full_page=True)

@pytest.fixture(scope="module")
def start_stop_server():
    # This fixture is a placeholder and doesn't actually start a server.
    # The server is expected to be running for these tests.
    # In a real-world scenario, this would be handled by a process manager.
    yield

@pytest.fixture(scope="module")
def sample_data():
    sample_data_path = "build/tests/sample-data.json"
    if not os.path.exists(sample_data_path):
        pytest.fail(f"Sample data file not found at {sample_data_path}")
    with open(sample_data_path, "r") as f:
        return json.load(f)

def login(page: Page, sample_data):
    page.goto("https://localhost:8443/welltrack/welltrack.html")
    page.evaluate(f"localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])}))")
    page.evaluate(f"localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])}))")
    page.evaluate(f"localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])}))")
    page.reload()
    page.wait_for_load_state("networkidle")

def logout(page: Page):
    page.evaluate("localStorage.clear()")
    page.reload()

def take_screenshots(page: Page, theme: str):
    output_dir = f"build/tests/darktheme/{theme}"
    os.makedirs(output_dir, exist_ok=True)

    tabs = ["today", "event", "mood", "pain", "history", "log", "settings"]
    for tab in tabs:
        page.goto(f"https://localhost:8443/welltrack/welltrack.html?page={tab}")
        page.wait_for_load_state("networkidle")
        make_screenshot(page, f"{output_dir}/{tab}.png")

def test_dark_theme_screenshots(start_stop_server, sample_data):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        context = browser.new_context(
            ignore_https_errors=True,
            locale="de-DE",
            timezone_id="Europe/Berlin",
            geolocation={"longitude": 48.208359954959, "latitude": 16.3723010569811},
            permissions=["geolocation", "notifications"],
            **p.devices["Pixel 7"],
        )
        page = context.new_page()
        login(page, sample_data)

        # Light theme
        page.evaluate("WellTrackApp.events.handleThemeChange('light')")
        take_screenshots(page, "light")

        # Dark theme
        page.evaluate("WellTrackApp.events.handleThemeChange('dark')")
        take_screenshots(page, "dark")

        logout(page)
        browser.close()