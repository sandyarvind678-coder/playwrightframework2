import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright


# --------------------------------------------------
# CLI OPTIONS
# --------------------------------------------------
def pytest_addoption(parser):
    parser.addoption("--browser", default="chromium")
    parser.addoption("--base-url", default="https://macktesting.solverminds.net/main")
    parser.addoption("--headed", action="store_true")
    parser.addoption("--video", default="retain-on-failure",
                     choices=["on", "off", "retain-on-failure"])
    parser.addoption("--screenshot", default="only-on-failure",
                     choices=["on", "off", "only-on-failure"])
    parser.addoption("--tracing", default="retain-on-failure",
                     choices=["on", "off", "retain-on-failure"])


# --------------------------------------------------
# TEST RESULT HOOK (REQUIRED)
# --------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


# --------------------------------------------------
# PLAYWRIGHT INSTANCE
# --------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


# --------------------------------------------------
# BROWSER
# --------------------------------------------------
@pytest.fixture(scope="session")
def browser(playwright_instance, pytestconfig):
    browser_name = pytestconfig.getoption("--browser")
    headed = pytestconfig.getoption("--headed")

    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=not headed)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=not headed)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=not headed)
    else:
        raise ValueError("Invalid browser")

    yield browser
    browser.close()


# --------------------------------------------------
# CONTEXT (VIDEO)
# --------------------------------------------------
@pytest.fixture()
def context(browser, pytestconfig):
    video = pytestconfig.getoption("--video")

    if video in ["on", "retain-on-failure"]:
        context = browser.new_context(record_video_dir="reports/videos")
    else:
        context = browser.new_context()

    yield context
    context.close()


# --------------------------------------------------
# PAGE (SCREENSHOT + TRACE)
# --------------------------------------------------
@pytest.fixture()
def page(context, pytestconfig, request):
    base_url = pytestconfig.getoption("--base-url")
    tracing = pytestconfig.getoption("--tracing")
    screenshot = pytestconfig.getoption("--screenshot")

    if tracing in ["on", "retain-on-failure"]:
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

    page = context.new_page()
    page.goto(base_url)

    yield page

    test_failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
    test_name = request.node.name

    # TRACE
    if tracing in ["on", "retain-on-failure"]:
        context.tracing.stop(path=f"reports/traces/{test_name}.zip")

    # SCREENSHOT (failure only)
    if test_failed and screenshot in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)

        allure.attach.file(
            screenshot_path,
            name=test_name,
            attachment_type=allure.attachment_type.PNG
        )
