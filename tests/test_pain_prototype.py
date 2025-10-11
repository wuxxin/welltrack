import re
from playwright.sync_api import Page, expect
import pytest
from pathlib import Path

def test_pain_prototype_screenshots(page: Page):
    # Use the file protocol to open the local prototype file
    # The path is relative to the root of the project where pytest is run
    file_path = Path.cwd() / "prototype" / "new-pain-entry.html"
    page.goto(file_path.as_uri())

    # Ensure the page has loaded correctly
    expect(page.get_by_text("Schmerzen")).to_be_visible()

    # Back view (default)
    page.screenshot(path="build/tests/output/pain_prototype_back.png")

    # Front view
    page.get_by_text("Vorderseite").click()
    expect(page.locator("#body-front")).to_be_visible()
    page.screenshot(path="build/tests/output/pain_prototype_front.png")

    # Other view
    page.get_by_text("Weitere").click()
    expect(page.locator("#body-other")).to_be_visible()
    page.screenshot(path="build/tests/output/pain_prototype_other.png")