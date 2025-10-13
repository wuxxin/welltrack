import re
import json
import pytest
from playwright.sync_api import Page, expect

# Constants
GERMAN_DATE_REGEX = re.compile(r"\w+ \d{1,2}\.\d{1,2}\.\d{4}")


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


def test_start_with_no_data(page: Page):
    """Test the application's initial state with no data in localStorage."""
    page.evaluate("() => localStorage.clear()")
    page.reload()

    # Check for "Heute" (Today) and the current date format.
    expect(page.locator("h2:has-text('Heute')")).to_be_visible()
    expect(page.locator("h2:has-text('Heute') + span")).to_have_text(GERMAN_DATE_REGEX)
    expect(page.get_by_text("Noch keine Einträge für Heute")).to_be_visible()


def test_start_with_empty_data(page: Page):
    """Test the application's initial state with empty data in localStorage."""
    page.evaluate(
        "() => { \
        localStorage.setItem('wellTrackMetrics', '[]'); \
        localStorage.setItem('wellTrackEventTypes', '[]'); \
        localStorage.setItem('wellTrackSettings', '{}'); \
    }"
    )
    page.reload()

    # Check for "Heute" (Today) and the current date format.
    expect(page.locator("h2:has-text('Heute')")).to_be_visible()
    expect(page.locator("h2:has-text('Heute') + span")).to_have_text(GERMAN_DATE_REGEX)
    expect(page.get_by_text("Noch keine Einträge für Heute")).to_be_visible()


def test_start_with_sample_data(page: Page, sample_data):
    """Test the application's state with sample data loaded from a file."""
    # Mock the current date to the last timestamp in the sample data
    last_timestamp = sample_data["metrics"][-1]["timestamp"]
    page.add_init_script(f"Date.now = () => {last_timestamp};")

    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    page.reload()
    page.wait_for_load_state("networkidle")

    # Navigate to the event page
    page.locator("#nav-event").click()
    page.wait_for_load_state("networkidle")

    # Click the correct event group to make the item visible
    page.locator("button:has-text('Ernährung')").click()
    page.wait_for_load_state("networkidle")

    # Check for a known entry from the sample data
    expect(page.locator("text=Kaffee Tassen").first).to_be_visible()


def test_settings_persistence(page: Page):
    """Test that changing a setting persists after a reload."""
    # Navigate to the pain page to check the default view
    page.locator("#nav-pain").click()
    expect(page.locator("#body-back")).to_be_visible()
    expect(page.locator("#body-front")).to_be_hidden()

    # Change the default pain view setting to 'front'
    page.locator("#btn-view-front").click()
    expect(page.locator("#body-front")).to_be_visible()
    expect(page.locator("#body-back")).to_be_hidden()

    # Reload the page and verify the setting has persisted
    page.reload()

    # Verify the setting in localStorage directly
    settings_json = page.evaluate("() => localStorage.getItem('wellTrackSettings')")
    settings = json.loads(settings_json)
    assert settings.get("painView") == "front"

    # Verify the UI reflects the persisted setting
    page.locator("#nav-pain").click()
    expect(page.locator("#body-front")).to_be_visible()
    expect(page.locator("#body-back")).to_be_hidden()


def test_main_navigation(page: Page, sample_data):
    """Test clicking through all main navigation icons and checking page titles."""
    page.evaluate(
        f"() => {{ \
        localStorage.setItem('wellTrackMetrics', JSON.stringify({json.dumps(sample_data['metrics'])})); \
        localStorage.setItem('wellTrackEventTypes', JSON.stringify({json.dumps(sample_data['eventTypes'])})); \
        localStorage.setItem('wellTrackSettings', JSON.stringify({json.dumps(sample_data['settings'])})); \
    }}"
    )
    page.reload()

    nav_items = {
        "event": "Ereignisse",
        "mood": "Stimmung",
        "pain": "Schmerzen",
        "history": "Verlauf",
        "log": "Protokoll",
        "settings": "Einstellungen",
        "today": "Heute",
    }

    for nav_id, title in nav_items.items():
        page.locator(f"#nav-{nav_id}").click()
        expect(page.locator(f"h2:has-text('{title}')")).to_be_visible()
