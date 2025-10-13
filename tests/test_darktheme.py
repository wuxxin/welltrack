import pytest
from playwright.sync_api import Page, expect
import os
import re

# Ensure the output directory exists
output_dir = "build/tests/darktheme"
os.makedirs(output_dir, exist_ok=True)

def set_theme(page: Page, theme: str):
    """Helper function to set the theme in localStorage."""
    page.evaluate(f"WellTrackApp.events.handleThemeChange('{theme}')")
    # Wait for the theme to be applied, you might need a better wait mechanism
    page.wait_for_timeout(500)

def test_dark_theme_screenshots(page: Page, live_server):
    """
    Test to take screenshots of all main tabs in both light and dark themes.
    """
    # Load sample data
    page.goto(f"{live_server}/welltrack/welltrack.html")
    with open("build/tests/sample-data.json", "r") as f:
        data_to_import = f.read()

    page.evaluate(f"""
        const data = {data_to_import};
        localStorage.setItem('wellTrackMetrics', JSON.stringify(data.metrics));
        localStorage.setItem('wellTrackEventTypes', JSON.stringify(data.eventTypes));
        localStorage.setItem('wellTrackSettings', JSON.stringify(data.settings));
        location.reload();
    """)
    page.wait_for_load_state("networkidle")

    tabs = ["today", "event", "mood", "pain", "history", "log", "settings"]
    themes = ["light", "dark"]

    for theme in themes:
        set_theme(page, theme)

        for tab in tabs:
            # Navigate to the tab
            page.click(f"#nav-{tab}")
            page.wait_for_timeout(500) # Wait for page to render

            # Take a screenshot
            screenshot_path = os.path.join(output_dir, f"{tab}_{theme}.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

            # Special case for settings to check all subtabs
            if tab == 'settings':
                settings_tabs = ["eventTypes", "data", "reminders", "display", "about"]
                for settings_tab in settings_tabs:
                    page.click(f"button[data-tab='{settings_tab}']")
                    page.wait_for_timeout(500)
                    screenshot_path = os.path.join(output_dir, f"settings_{settings_tab}_{theme}.png")
                    page.screenshot(path=screenshot_path, full_page=True)
                    print(f"Screenshot saved to {screenshot_path}")