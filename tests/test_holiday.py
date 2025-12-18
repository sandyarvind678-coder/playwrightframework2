from playwright.sync_api import expect, Playwright


def test_brcontext(playwright:Playwright):
    browser= playwright.chromium.launch(headless=False)
    context=browser.new_context()

    page=context.new_page()
    page1 = context.new_page()


    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_timeout(5000)
    page1.goto("https://testautomationpractice.blogspot.com/")
    page1.wait_for_timeout(5000)
