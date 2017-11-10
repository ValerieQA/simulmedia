from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.by import By


class BasePage(object):
    url = None

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def navigate(self):
        self.driver.get(self.url)
        self.verify()

    def verify(self):
        pass

    def get_title(self):
        return self.driver.title


class SimulmediaPage(BasePage):
    url = "http://a7.simulmedia.com/OpenAccess"

    def verify(self):
        self.wait.until(EC.title_contains('Simulmedia'))

    def get_header(self):
        return self.driver.find_element_by_xpath('//table[@class="oa-OverviewBar"]').text

    def get_footer(self):
        return self.driver.find_element_by_xpath('//div[@class="oa-Footer"]/table').text

    def _get_selected_tab(self):
        return self.driver.find_element_by_xpath('//div[contains(@class, "oa-Header-Button-Selected")]/div')

    def _get_research_tab(self):
        return self.driver.find_element_by_xpath('//div[contains(@class, "oa-Header-Button")]/div[text()="Research"]')

    def _get_plan_tab(self):
        return self.driver.find_element_by_xpath('//div[contains(@class, "oa-Header-Button")]/div[text()="Plan"]')

    def _getinfo(self, webelement):
        AC(self.driver).move_to_element(webelement).perform()
        return self.driver.find_element_by_xpath('//span[@id="fusioncharts-tooltip-element"]').text

    def get_research_page(self):
        if self._get_research_tab() != self._get_selected_tab():
            self._get_research_tab().click()
        return ResearchPage(self.driver, self.wait)

    def get_plan_page(self):
        if self._get_plan_tab() != self._get_selected_tab():
            self._get_plan_tab().click()
        return PlanPage(self.driver, self.wait)


class ResearchPage(SimulmediaPage):
    url = 'http://a7.simulmedia.com/OpenAccess/#OpenAccess:BrandAnalytics:0'

    def verify(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="GD5OOFGDOK"]/table/tbody/tr[4]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][1]')))

    def set_brand(self, text):
        brand_textbox = self.driver.find_element_by_xpath('//input[contains(@class,"sm-SuggestionTextBox-SearchBox")]')
        brand_textbox.clear()
        brand_textbox.send_keys(text)

        brand_textbox_suggestion_item = self.driver.find_element_by_xpath('//table[contains(@class, "sm-SingleSelectScrollList-Items")]/tbody/tr[1]/td/div')
        brand_textbox_suggestion_item.click()

    def set_audience(self, text):
        audience_dropdown_item = self.driver.find_element_by_xpath('//select[@class="gwt-ListBox oa-ContextBarItem-Widget"]/option[@value="' + text + '"]')
        audience_dropdown_item.click()

    def set_year(self, year):
        self.driver.find_element_by_xpath('//table[@class = "oa-ChartTitleBar"]//option[@value="' + str(year) + '"]').click()

    def set_month(self, month):
        self.driver.find_element_by_xpath('//table[contains(@class, "oa-MonthSelectorBar")]//option[' + str(month) + ']').click()

    def get_reach_by_month(self, month):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[4]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][' + str(month) + ']')
        return self._getinfo(element)

    def get_frequency_by_month(self, month):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[4]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="circle"][' + str(month) + ']')
        return self._getinfo(element)

    def get_unduplicated_reach_by_network(self, network):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[7]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][' + str(network) + ']')
        return self._getinfo(element)

    def get_duplicated_reach_by_network(self, network):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[7]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][count(../*[name()="rect"]) * 0.5 + ' + str(network) + ']')
        return self._getinfo(element)

    def get_cost_by_network(self, network):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[7]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="circle"][' + str(network) + ']')
        return self._getinfo(element)

    def get_reached_by_daypart(self, daypart):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[10]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][' + str(daypart) + ']')
        return self._getinfo(element)

    def get_unreached_by_daypart(self, daypart):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[10]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][count(../*[name()="rect"]) * 0.5 + ' + str(daypart) + ']')
        return self._getinfo(element)

    def get_cost_by_daypart(self, daypart):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[10]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="circle"][' + str(daypart) + ']')
        return self._getinfo(element)

    def get_reach_by_quintile(self, quintile):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[10]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[' + str(quintile + 1) + ']/td[2]/div')
        return element.get_attribute("title")

    def get_frequency_by_quintile(self, quintile):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[10]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/div/table/tbody/tr[' + str(quintile + 1) + ']/td[4]/table')
        return element.get_attribute("title")


class PlanPage(SimulmediaPage):
    url = 'http://a7.simulmedia.com/OpenAccess/#OpenAccess:Action:0'

    def verify(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="GD5OOFGDOK"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[not(contains(@class, "loading"))]/tbody/tr[2]/td[2]/div')))

    def set_start_date(self, date):
        date_textbox = self.driver.find_element_by_xpath('//table[@ class="oa-ContextBarItem-Widget"]/tbody/tr/td[1]//input[@class="sm-IconBox-TextBox"]')
        date_textbox.clear()
        date_textbox.send_keys(date)

    def set_end_date(self, date):
        date_textbox = self.driver.find_element_by_xpath('//table[@ class="oa-ContextBarItem-Widget"]/tbody/tr/td[3]//input[@class="sm-IconBox-TextBox"]')
        date_textbox.clear()
        date_textbox.send_keys(date)

    def set_budget_amount(self, amount):
        budget_textbox = self.driver.find_element_by_xpath('//table[@ class="oa-ContextBarItem-Widget"]/tbody/tr/td[1]//input[@class="gwt-TextBox sm-NumericTextBox"]')
        budget_textbox.clear()
        budget_textbox.send_keys(amount)

    def set_budget_type(self, netgross):
        self.driver.find_element_by_xpath('//select[@class="gwt-ListBox"]/option[@value="' + netgross + '"]').click()

    def set_audience(self, audience):
        self.driver.find_element_by_xpath('//select[@class="gwt-ListBox oa-ContextBarItem-Widget"]/option[@value="' + audience + '"]').click()

    def get_grps(self):
        return self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[not(contains(@class, "loading"))]/tbody/tr[2]/td[2]/div').text

    def get_cpm(self):
        return self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[not(contains(@class, "loading"))]/tbody/tr[3]/td[2]/div').text

    def get_reach(self):
        return self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[not(contains(@class, "loading"))]/tbody/tr[4]/td[2]/div').text

    def get_impressions(self):
        return self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table[not(contains(@class, "loading"))]/tbody/tr[5]/td[2]/div').text

    def get_impressions_by_day(self, day):
        element = self.driver.find_element_by_xpath('//div[@class="GD5OOFGDOK"]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div[not(contains(@class, "loading"))]/div/div/span/*[name()="svg"]/*[name()="g"][8]/*[name()="rect"][' + str(day) + ']')
        return self._getinfo(element)
