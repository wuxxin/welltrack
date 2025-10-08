import json
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def sample_data():
    """Fixture to load sample data from file."""
    with open("build/tests/sample-data.json", "r") as f:
        return json.load(f)

@pytest.fixture
def page(page: Page, live_server):
    """Fixture to configure the browser page and navigate to the app."""
    page.goto(f"{live_server}/welltrack/welltrack.html", wait_until="networkidle")
    return page

def test_take_heute_screenshot_before(page: Page, sample_data):
    """Test to take a screenshot of the 'Heute' page with sample data."""
    # Load sample data into localStorage
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    # Reload the page to ensure the data is loaded and rendered
    page.reload(wait_until="networkidle")

    # Ensure the "Heute" page is visible
    expect(page.locator("h2:has-text('Heute')")).to_be_visible()

    # Take a full-page screenshot
    page.screenshot(path="build/tests/screenshots/heute-before.png", full_page=True)

def test_take_heute_screenshot_after(page: Page, sample_data):
    """Test to take a screenshot of the 'Heute' page with sample data after changes."""
    # Load sample data into localStorage
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    # Reload the page to ensure the data is loaded and rendered
    page.reload(wait_until="networkidle")

    # Ensure the "Heute" page is visible
    expect(page.locator("h2:has-text('Heute')")).to_be_visible()

    # Take a full-page screenshot
    page.screenshot(path="build/tests/screenshots/heute-after.png", full_page=True)

def test_take_protokoll_screenshot_before(page: Page, sample_data):
    """Test to take a screenshot of the 'Protokoll' page with sample data."""
    # Load sample data into localStorage
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    # Reload the page to ensure the data is loaded and rendered
    page.reload(wait_until="networkidle")

    # Navigate to the log page
    page.locator("#nav-log").click()
    expect(page.locator("h2:has-text('Protokoll')")).to_be_visible()

    # Take a full-page screenshot
    page.screenshot(path="build/tests/screenshots/protokoll-before.png", full_page=True)

def test_take_protokoll_screenshot_after(page: Page, sample_data):
    """Test to take a screenshot of the 'Protokoll' page with sample data after refactoring."""
    # Load sample data into localStorage
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    # Reload the page to ensure the data is loaded and rendered
    page.reload(wait_until="networkidle")

    # Navigate to the log page
    page.locator("#nav-log").click()
    expect(page.locator("h2:has-text('Protokoll')")).to_be_visible()

    # Take a full-page screenshot
    page.screenshot(path="build/tests/screenshots/protokoll-after.png", full_page=True)

def test_take_settings_screenshot_before(page: Page, sample_data):
    """Test to take a screenshot of the 'Settings' page with sample data."""
    # Load sample data into localStorage
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    # Reload the page to ensure the data is loaded and rendered
    page.reload(wait_until="networkidle")

    # Navigate to the settings page
    page.locator("#nav-settings").click()
    expect(page.locator("h2:has-text('Einstellungen')")).to_be_visible()

    # Take a full-page screenshot
    page.screenshot(path="build/tests/screenshots/settings-before.png", full_page=True)

def test_take_settings_screenshot_after(page: Page, sample_data):
    """Test to take a screenshot of the 'Settings' page after triggering a rebirth message."""
    # Load sample data into localStorage
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    page.reload(wait_until="networkidle")

    # Navigate to the settings page to ensure the app is in the correct state
    page.locator("#nav-settings").click()
    expect(page.locator("h2:has-text('Einstellungen')")).to_be_visible()

    # Expect a navigation to happen when we call the function that reloads the page.
    with page.expect_navigation():
        page.evaluate("() => WellTrackApp.events.saveDayStartTime('06:00')")

    # After the reload, wait for the rebirth message to appear
    expect(page.locator("#rebirth-message-overlay")).to_be_visible()
    expect(page.locator("#rebirth-message-text")).to_have_text("Neuer Tag beginnt jetzt um 06:00.")

    # Take a screenshot
    page.screenshot(path="build/tests/screenshots/settings-after.png", full_page=True)