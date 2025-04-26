# tests/test_smoke.py

from playwright.sync_api import sync_playwright

def test_homepage_loads_and_shows_login():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5000")

        # More specific locator:
        login_link = page.locator('nav.site-nav a[href="/login"]')
        assert login_link.is_visible()

        browser.close()
