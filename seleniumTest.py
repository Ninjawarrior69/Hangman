import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

## TESTS DONE BY JOSH COOPER

class BarChartTest(unittest.TestCase):
    def setUp(self):
        #opening web driver in chrome
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # Closing the browser
        self.driver.quit()

    def test_bar_chart_loading(self):
        # find the chart page
        self.driver.get("http://127.0.0.1:5000/charts")

        #get  bar chart by ID
        barChart = self.driver.find_element(By.ID,"barChart")

        # check if displayed 
        self.assertTrue(barChart.is_displayed())


    def test_ExistingFeedback_loading(self):
        # same as before but for the existing feedback
        self.driver.get("http://127.0.0.1:5000/ExistingFeedback")

        
        ExistingFeedbackTable = self.driver.find_element(By.CLASS_NAME,"Feedbacktable")

        
        self.assertTrue(ExistingFeedbackTable.is_displayed())


    def test_check_CSRF_token_and_form_loads_LOGIN(self):
        self.driver.get("http://127.0.0.1:5000/login")


        Token = self.driver.find_elements(By.NAME,"csrf_token")

        self.assertIsNotNone(Token)       # A  CSRF TOKEN CORRECTLY RENDERS


    
    def test_check_CSRF_token_and_form_loads_SIGNUP(self):
        self.driver.get("http://127.0.0.1:5000/signup")


        Token = self.driver.find_elements(By.NAME,"csrf_token")

        self.assertIsNotNone(Token)       # A  CSRF TOKEN CORRECTLY RENDERS

if __name__ == "__main__":
    unittest.main()