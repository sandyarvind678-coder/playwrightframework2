import pytest
from pages.loginpage import LoginPage
from utils.excel_reader import read_excel_data
from pages.holidaycalendarpage import HolidayPage

@pytest.mark.sanity
@pytest.mark.parametrize(
    "sheet_name,username,password,modulesearch,agreement",
    read_excel_data(
        r"D:\Automationfile\playwrightcsvfile\playwrightexceldata.xlsx",
        "Sheet1"
    )
)
def test_login(page, sheet_name, username, password, modulesearch, agreement):

    login = LoginPage(page)
    holiday = HolidayPage(page)

    # 🔹 Login only if credentials are provided
    if username and password:
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()

    # 🔹 Module search only if value is provided
    if modulesearch:
        holiday.enter_modulesearch(modulesearch)
        holiday.moduleselectpage()

    # 🔹 Agreement selection only if value is provided
    if agreement:
        holiday.agreementselection()
        holiday.agreementsearch12(agreement)
        holiday.agreementselectname(agreement)

    page.wait_for_timeout(5000)






