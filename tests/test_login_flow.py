# tests/test_login_flow.py

from playwright.sync_api import sync_playwright

def test_login_page_toggles_forms():
    """
    - Navigates to /login
    - Verifies the Log In form is visible by default
    - Clicks the 'Create Account' button and checks the signup form appears
    - Clicks back to 'Log In' and verifies the login form is back
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()

        # 1. Go to the login page
        page.goto("http://localhost:5000/login")

        # 2. By default, login form should show
        assert page.locator("form#login-form.active").is_visible()
        assert page.locator("text=Log In").first.is_visible()

        # 3. Click 'Create Account' toggle
        page.click("button:has-text('Create Account')")
        # Now signup form should have .active
        assert page.locator("form#signup-form.active").is_visible()
        assert page.locator("text=Create Account").first.is_visible()

        # 4. Click back to 'Log In'
        page.click("button:has-text('Log In')")
        assert page.locator("form#login-form.active").is_visible()

        browser.close()
