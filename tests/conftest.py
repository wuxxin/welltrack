import pytest
import subprocess
import time

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
def browser_context_args(browser_context_args):
    """
    Fixture to configure browser context.

    This fixture sets the `ignore_https_errors` option to True, which allows
    Playwright to work with self-signed certificates used by the dev server.
    """
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }