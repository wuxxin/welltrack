import re
from playwright.sync_api import Page, expect
import pytest
import os

# Ensure the output directory exists
os.makedirs("build/tests/output", exist_ok=True)

def test_ui_screenshots(page: Page, live_server):
    page.goto(f"{live_server}/welltrack/welltrack.html")

    # Inject sample data
    sample_data_path = os.path.join(os.path.dirname(__file__), '..', 'build', 'tests', 'sample-data.json')
    with open(sample_data_path, 'r') as f:
        sample_data = f.read()

    page.evaluate(f"""
        localStorage.setItem('wellTrackMetrics', JSON.stringify({sample_data}));
        localStorage.setItem('wellTrackEventTypes', JSON.stringify([]));
        localStorage.setItem('wellTrackSettings', JSON.stringify({{...JSON.parse(localStorage.getItem('wellTrackSettings') || '{{}}'), theme: 'light'}}));
    """)
    page.reload()

    tabs = ["today", "event", "mood", "pain", "history", "log", "settings"]

    # --- Light Mode Screenshots ---
    page.evaluate("WellTrackApp.events.applyTheme('light')")
    page.wait_for_timeout(500) # Wait for theme to apply
    for tab in tabs:
        page.click(f"#nav-{tab}")
        page.wait_for_timeout(500) # Wait for page to render
        page.screenshot(path=f"build/tests/output/screenshot_{tab}_light.png", full_page=True)

    # --- Dark Mode Screenshots ---
    page.evaluate("WellTrackApp.events.applyTheme('dark')")
    page.wait_for_timeout(500) # Wait for theme to apply
    for tab in tabs:
        page.click(f"#nav-{tab}")
        page.wait_for_timeout(500) # Wait for page to render
        page.screenshot(path=f"build/tests/output/screenshot_{tab}_dark.png", full_page=True)