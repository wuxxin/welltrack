import pytest
import subprocess
import time
from playwright.sync_api import Playwright
import os


@pytest.fixture(scope="session", autouse=True)
def create_sample_data_if_not_exists():
    """Fixture to ensure sample data exists before tests run."""
    sample_data_path = "build/tests/sample-data.json"
    if not os.path.exists(sample_data_path):
        os.makedirs("build/tests", exist_ok=True)
        subprocess.run(
            [".venv/bin/python", "scripts/create-sample-data.py", sample_data_path],
            check=True,
        )


@pytest.fixture(scope="session")
def live_server():
    """Fixture to start a live server for the test session."""
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
    """Fixture to configure browser context"""
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
