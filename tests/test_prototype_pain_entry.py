import pytest
from playwright.sync_api import Page, expect
import os
import re

def test_prototype_pain_entry_screenshots(page: Page):
    """
    Test to verify the new pain entry prototype and generate screenshots.
    """
    # Get absolute path to the prototype file
    basedir = os.getcwd()
    file_url = f"file://{basedir}/src/prototype/new-pain-entry.html"

    output_dir = "build/tests/new-pain-entry"
    os.makedirs(output_dir, exist_ok=True)

    # Open the prototype
    page.goto(file_url)

    # 1. Back View (Default)
    expect(page.get_by_role("button", name="Rückseite")).to_have_class(re.compile(r"active"))
    page.screenshot(path=f"{output_dir}/pain_entry_back.png", full_page=True)

    # 2. Front View
    page.get_by_role("button", name="Vorderseite").click()
    expect(page.get_by_role("button", name="Vorderseite")).to_have_class(re.compile(r"active"))
    # Wait for transition if any, though simple toggle should be fast
    page.wait_for_timeout(200)
    page.screenshot(path=f"{output_dir}/pain_entry_front.png", full_page=True)

    # 3. Other View
    page.get_by_role("button", name="Weitere").click()
    expect(page.get_by_role("button", name="Weitere")).to_have_class(re.compile(r"active"))
    page.wait_for_timeout(200)
    page.screenshot(path=f"{output_dir}/pain_entry_other.png", full_page=True)

    # 4. Settings View
    # Use title selector as the button has no text
    page.get_by_title("Einstellungen").click()
    page.wait_for_timeout(200)
    page.screenshot(path=f"{output_dir}/settings.png", full_page=True)
