import re
from playwright.sync_api import Page, expect
import pytest

def test_new_pain_entry_prototype(page: Page, live_server):
    page.goto(live_server + "/prototype/new-pain-entry.html")

    # Test front view is active by default
    expect(page.locator("#btn-view-front")).to_have_class(re.compile(r'active'))
    page.screenshot(path="build/tests/output/new-pain-entry-front.png")

    # Test back view
    page.locator("#btn-view-back").click()
    expect(page.locator("#btn-view-back")).to_have_class(re.compile(r'active'))
    page.screenshot(path="build/tests/output/new-pain-entry-back.png")

    # Test head_hands_feets view
    page.locator("#btn-view-head_hands_feets").click()
    expect(page.locator("#btn-view-head_hands_feets")).to_have_class(re.compile(r'active'))
    page.screenshot(path="build/tests/output/new-pain-entry-head_hands_feets.png")

    # Test other view
    page.locator("#btn-view-other").click()
    expect(page.locator("#btn-view-other")).to_have_class(re.compile(r'active'))
    page.screenshot(path="build/tests/output/new-pain-entry-other.png")