import re
from playwright.sync_api import sync_playwright, expect
import os

def test_pain_entry_prototype(page):
    """Test the pain entry prototype."""
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = f"file://{basedir}/dev/prototype/new-pain-entry.html"
    page.goto(file_path)

    # Create directory for screenshots
    os.makedirs("build/tests/new-pain-entry", exist_ok=True)

    # Take screenshot of the front view
    page.locator("#btn-view-front").click()
    page.screenshot(path="build/tests/new-pain-entry/front.png")

    # Take screenshot of the back view
    page.locator("#btn-view-back").click()
    page.screenshot(path="build/tests/new-pain-entry/back.png")

    # Take screenshot of the other view
    page.locator("#btn-view-other").click()
    page.screenshot(path="build/tests/new-pain-entry/other.png")