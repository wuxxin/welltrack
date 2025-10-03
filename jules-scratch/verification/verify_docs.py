import re
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)  # Ignore self-signed cert error
    page = context.new_page()

    try:
        # 1. Navigate directly to the new documentation page.
        # mkdocs usually creates clean URLs from the file path.
        page.goto("https://devbox:8443/docs/mood-and-pain/")

        # 2. Verify that the correct page is loaded by checking the main heading.
        heading = page.get_by_role("heading", name="Leitfaden zur Erfassung von Stimmung und Schmerz")
        expect(heading).to_be_visible()

        # 3. Take a screenshot for verification.
        page.screenshot(path="jules-scratch/verification/docs-verification.png")

        print("Verification script completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)