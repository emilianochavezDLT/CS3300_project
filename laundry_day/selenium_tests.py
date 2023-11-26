from selenium import webdriver
from django.test import LiveServerTestCase

class MySeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def tearDown(self):
        self.driver.quit()

    def test_title(self):
        self.driver.get(self.live_server_url)
        assert 'Laundry Day' in self.driver.title