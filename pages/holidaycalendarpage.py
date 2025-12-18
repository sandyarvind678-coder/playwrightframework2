from playwright.sync_api import Page

class HolidayPage:

    def __init__(self, page: Page):
        self.page = page

        # Module search
        self.modulesearch_input = page.locator(
            "#NFR_megamenu-nfr_topbar_autocomp1_input"
        )

        # Module result (avoid ui-state-highlight)
        self.mselectpage = page.locator(
            "//li[contains(@class,'ui-autocomplete-item')]"
        )

        # Agreement dropdown
        self.agreement_dropdown = page.locator(
            "#HLC-HLC_CodeAndAgreement_label"
        )

        # Agreement search input
        self.agreementsearch1 = page.locator(
            "#HLC-HLC_CodeAndAgreement_filter"
        )

    def enter_modulesearch(self, ms: str):
        self.modulesearch_input.fill(ms)

    def moduleselectpage(self):
        self.mselectpage.first.click()

    def agreementselection(self):
        self.agreement_dropdown.click()

    def agreementsearch12(self, asg: str):
        self.agreementsearch1.fill(asg)

    def agreementselectname(self, agreement: str):
        self.page.get_by_role(
            "option",
            name=agreement,
            exact=True
        ).first.click()








