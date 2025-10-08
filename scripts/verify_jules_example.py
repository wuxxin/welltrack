#!/usr/bin/env python
"""Jules Playwright GUI Verify Examplefor WellTrack"""

import re
from playwright.sync_api import Page, expect, sync_playwright


def test_welltrack_eventtype_layout(page: Page):
    # Load sample data
    page.goto("https://localhost:8443/welltrack/welltrack.html", timeout=60000)
    page.locator("#nav-settings").click()
    page.locator("button[data-tab='data']").click()
    expect(page.locator("#settings-tab-data")).to_be_visible()

    with page.expect_file_chooser() as fc_info:
        page.locator("label:has-text('Daten importieren')").click()

    file_chooser = fc_info.value
    file_chooser.set_files("build/tests/sample-data.json")

    page.get_by_role("button", name="Daten überschreiben").click()
    expect(page.locator("#today-summary-cards")).to_be_visible(timeout=10000)

    # Verify Alternating Styles & Layout in Settings -> EventTypes
    page.locator("#nav-settings").click()
    page.locator("button[data-tab='eventTypes']").click()
    expect(page.locator("#manage-event-list")).to_be_visible()
    page.screenshot(
        path="jules-scratch/verification/updated_event_types_view.png", full_page=True
    )


def run_test():
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
        try:
            test_welltrack_eventtype_layout(page)
            print("Verification script ran successfully.")
        except Exception as e:
            print(f"Verification script failed: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run_test()
