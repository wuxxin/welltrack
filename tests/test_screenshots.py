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


def test_take_heute_screenshot_(page: Page, sample_data):
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
    page.screenshot(path="build/tests/output/heute.png", full_page=True)


def test_take_protokoll_screenshot_(page: Page, sample_data):
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
    page.screenshot(path="build/tests/output/protokoll.png", full_page=True)


def test_take_settings_screenshot_(page: Page, sample_data):
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
    page.screenshot(path="build/tests/output/settings.png", full_page=True)
