from playwright.sync_api import Page

class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#NFR_LoginForm-nfr_login_authname")
        self.password_input = page.locator("#NFR_LoginForm-nfr_login_authid")
        self.login_button = page.locator("#NFR_LoginForm-nfr_login_btnlogin")
        self.modulesearch_input= page.locator("#NFR_megamenu-nfr_topbar_autocomp1_input")

    def enter_username(self, uname: str):
        self.username_input.fill(uname)

    def enter_password(self, pwd: str):
        self.password_input.fill(pwd)

    def click_login(self):
        self.login_button.click()

    def enter_modulesearch(self,ms: str):
        self.modulesearch_input.fill(ms)

    def select_date(self, selDate, selMonth, selYear, is_future):
        max_tries = 24
        attempts = 0

        while attempts < max_tries:
            current_month = self.page.locator(
                ".ui-datepicker-month"
            ).inner_text().strip()

            current_year = self.page.locator(
                ".ui-datepicker-year"
            ).inner_text().strip()

            if current_month == selMonth and current_year == selYear:
                break

            if is_future:
                self.page.locator("a[data-handler='next']").click()
            else:
                self.page.locator("a[data-handler='prev']").click()

            attempts += 1

        self.page.locator(
            f"//td[not(contains(@class,'ui-datepicker-other-month'))]"
            f"/a[text()='{selDate}']"
        ).click()