import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from PycharmProjects.Simulmedia.PageObject import ResearchPage, PlanPage


class SimulmediaTest(unittest.TestCase):

    driver = None
    wait = None

    @classmethod
    def setUpClass(cls):
        print("Opening Browser")
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)

    def test_research_page(self):
        page = ResearchPage(self.driver, self.wait)
        page.navigate()
        page.set_brand("WALMART")
        page.set_audience("M18-49")
        page.set_year(2012)
        page.set_month(8)
        assert page.get_reach_by_month(1) == "Reach, 1/2012, 50.41M", page.get_reach_by_month(1)
        assert page.get_frequency_by_month(1) == "Frequency, 1/2012, 11.2"
        assert page.get_unduplicated_reach_by_network(1) == "Unduplicated Reach, NBC, 3.7M"
        assert page.get_duplicated_reach_by_network(1) == "Duplicated Reach, NBC, 26.44M"
        assert page.get_cost_by_network(1) == "Cost, NBC, $530.14"
        assert page.get_reach_by_quintile(1) == "Average Frequency, 100% Quintile, 0.3"
        assert page.get_frequency_by_quintile(1) == "Percentage of Impressions, 100% Quintile, 0.5%"
        assert page.get_reached_by_daypart(1) == "Reached, Late Night, 22,826,615"
        assert page.get_unreached_by_daypart(1) == "Unreached, Late Night, 25,179,222"
        assert page.get_cost_by_daypart(1) == "Cost, Late Night, $104"

    def test_plan_page(self):
        page = PlanPage(self.driver, self.wait)
        page.navigate()
        page.set_start_date("2015-09-25")
        page.set_end_date("2015-09-30")
        page.set_budget_amount("$5.000.000")
        page.set_budget_type("Gross")
        page.set_audience("A18-54 (Breakfast Bar Consumers)")
        assert page.get_grps() == "449.07", page.get_grps()
        assert page.get_cpm() == "$34.96"
        assert page.get_reach() == "23,377,390"
        assert page.get_impressions() == "121,562,429"
        assert page.get_impressions_by_day(1) == "Forecasted Daily Impressions, 9/25, 18.96M"

    @classmethod
    def tearDownClass(cls):
        print("Closing Browser")
        cls.driver.close()
        pass
