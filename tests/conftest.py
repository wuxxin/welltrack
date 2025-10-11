import pytest
import subprocess
import time
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def live_server():
    """Starts and tears down a live server for the test session.

    This pytest fixture starts the development server using `scripts/dev_serve.py`
    at the beginning of a test session and ensures it's terminated afterward.
    It serves the files from the `build/site` directory, which is necessary
    for end-to-end GUI tests.

    Yields:
        str: The base URL of the live server (e.g., 'https://localhost:8443').
    """
    port = 8443
    command = ["python", "scripts/dev_serve.py", "-d", "build/site", str(port)]

    # Start the server as a subprocess
    server_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give the server a moment to start
    time.sleep(2)

    # Yield the base URL
    yield f"https://localhost:{port}"

    # Teardown: stop the server
    server_process.terminate()
    server_process.wait()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright: Playwright):
    """Configures the browser context for Playwright tests.

    This fixture extends the default browser context arguments provided by
    pytest-playwright. It sets up the browser to emulate a 'Pixel 7' device,
    ignore HTTPS errors from the self-signed certificate, and sets a German
    locale and timezone to match the application's target audience.

    Args:
        browser_context_args (dict): The default browser context arguments.
        playwright (Playwright): The Playwright instance.

    Returns:
        dict: The updated dictionary of browser context arguments.
    """
    pixel_7 = playwright.devices["Pixel 7"]
    return {
        **browser_context_args,
        **pixel_7,
        "ignore_https_errors": True,
        "locale": "de-DE",
        "timezone_id": "Europe/Berlin",
        "geolocation": {"longitude": 48.208359954959, "latitude": 16.3723010569811},
        "permissions": ["geolocation", "notifications"],
    }
