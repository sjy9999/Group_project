from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from app import app, db

class TestFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create Flask application context and push it
        cls.app_context = app.app_context()
        cls.app_context.push()

        # Create database tables
        db.create_all()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def test_register_and_login(self):
        self.driver.get("http://127.0.0.1:5000/access/")

        # Fill in the registration form
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field = self.driver.find_element(By.ID, "email")
        password_field = self.driver.find_element(By.ID, "password")

        username_field.send_keys("testuser")
        email_field.send_keys("testuser@example.com")
        password_field.send_keys("password")

        # Submit the registration form
        register_button = self.driver.find_element(By.NAME, "register")
        register_button.click()

        # Wait for redirect to the student page
        try:
            self.wait.until(EC.url_to_be("http://127.0.0.1:5000/student"))
            print("Registration successful.")
        except Exception as e:
            print(f"Registration error: {e}")
            print(f"Current URL after exception: {self.driver.current_url}")
            self.fail("Registration failed. Did not redirect to student page.")

        # Navigate back to the access page
        self.driver.get("http://127.0.0.1:5000/access/")

        # Fill in the login form
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username1")))
        password_field = self.driver.find_element(By.ID, "passwordLogin")

        username_field.send_keys("testuser")
        password_field.send_keys("password")

        # Submit the login form
        login_button = self.driver.find_element(By.NAME, "login")
        login_button.click()

        # Check for successful login by verifying the URL
        try:
            self.wait.until(EC.url_contains("main"))
            self.assertIn("main", self.driver.current_url)
            print("Login successful.")
        except Exception as e:
            print(f"Login error: {e}")
            self.fail("Login failed. Did not redirect to main page.")

    def test_create_request(self):
        # Log in to access the create request functionality
        self.driver.get("http://127.0.0.1:5000/access/")

        # Fill in the login form
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username1")))
        password_field = self.driver.find_element(By.ID, "passwordLogin")

        username_field.send_keys("testuser")
        password_field.send_keys("password")

        # Submit the login form
        login_button = self.driver.find_element(By.NAME, "login")
        login_button.click()

        # Check for successful login by verifying the URL
        try:
            self.wait.until(EC.url_contains("main"))
            self.assertIn("main", self.driver.current_url)
            print("Login successful.")
        except Exception as e:
            print(f"Login error: {e}")
            self.fail("Login failed. Did not redirect to main page.")

        # Navigate to the create request page
        self.driver.get("http://127.0.0.1:5000/createRequest")

        # Fill in the create request form
        title_field = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        description_field = self.driver.find_element(By.ID, "description")

        title_field.send_keys("This Test Request Title")
        description_field.send_keys("This is a description for the test request.")

        # Submit the create request form
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-custom')]")
        submit_button.click()

        # Check for successful request creation by verifying a success message or redirect URL
        try:
            self.wait.until(EC.url_contains("main"))
            self.assertIn("main", self.driver.current_url)
            print("Request creation successful.")
        except Exception as e:
            print(f"Request creation error: {e}")
            self.fail("Request creation failed. Did not redirect to main page.")


    def test_find_request(self):
        driver = self.driver

        # Log in to access the find request functionality
        driver.get("http://127.0.0.1:5000/access/")

        # Fill in the login form
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username1")))
        password_field = driver.find_element(By.ID, "passwordLogin")

        username_field.send_keys("testuser")
        password_field.send_keys("password")

        # Submit the login form
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Check for successful login by verifying the URL
        try:
            self.wait.until(EC.url_contains("main"))
            self.assertIn("main", driver.current_url)
            print("Login successful.")
        except Exception as e:
            print(f"Login error: {e}")
            self.fail("Login failed. Did not redirect to main page.")

        # Navigate to the find request page
        driver.get("http://127.0.0.1:5000/findRequest")

        # Fill in the search form
        search_query_field = self.wait.until(EC.presence_of_element_located((By.NAME, "searchQueryFR")))
        search_query_field.send_keys("test")

        # Submit the search form
        search_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
        search_button.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))

        # Check if still on the findRequest page
        try:
            current_url = driver.current_url
            self.assertIn("findRequest", current_url)
            print("Find request successful.")
        except Exception as e:
            print(f"Find request error: {e}")
            print(f"Current URL: {current_url}")  # Print the current URL for debugging
            self.fail("Find request failed. Did not stay on findRequest page.")


    def test_ranking_page(self):
        driver = self.driver

        # Log in to access the ranking functionality
        driver.get("http://127.0.0.1:5000/access/")

        # Fill in the login form
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username1")))
        password_field = driver.find_element(By.ID, "passwordLogin")

        username_field.send_keys("testuser")
        password_field.send_keys("password")

        # Submit the login form
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Check for successful login by verifying the URL
        try:
            self.wait.until(EC.url_contains("main"))
            self.assertIn("main", driver.current_url)
            print("Login successful.")
        except Exception as e:
            print(f"Login error: {e}")
            self.fail("Login failed. Did not redirect to main page.")

        # Navigate to the ranking page
        driver.get("http://127.0.0.1:5000/Ranking")

        # Check if still on the ranking page
        try:
            current_url = driver.current_url
            self.assertIn("Ranking", current_url)
            print("Ranking page access successful.")
        except Exception as e:
            print(f"Ranking page access error: {e}")
            print(f"Current URL: {current_url}")  # Print the current URL for debugging
            self.fail("Ranking page access failed. Did not stay on ranking page.")


    def test_login_logout(self):
        driver = self.driver

        # Log in to access the dashboard and logout functionality
        driver.get("http://127.0.0.1:5000/access/")

        # Fill in the login form
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username1")))
        password_field = driver.find_element(By.ID, "passwordLogin")

        username_field.send_keys("testuser")
        password_field.send_keys("password")

        # Submit the login form
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Check for successful login by verifying the URL
        try:
            self.wait.until(EC.url_contains("main"))
            self.assertIn("main", driver.current_url)
            print("Login successful.")
        except Exception as e:
            print(f"Login error: {e}")
            self.fail("Login failed. Did not redirect to main page.")

        # Navigate to the dashboard page
        driver.get("http://127.0.0.1:5000/dashboard")

        # Check if still on the dashboard page
        try:
            current_url = driver.current_url
            self.assertIn("dashboard", current_url)
            print("Dashboard access successful.")
        except Exception as e:
            print(f"Dashboard access error: {e}")
            print(f"Current URL: {current_url}")  # Print the current URL for debugging
            self.fail("Dashboard access failed. Did not stay on dashboard page.")

        # Perform logout
        logout_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Logout']")))
        logout_button.click()

        # Check if successfully logged out by verifying the URL
        try:
            self.wait.until(EC.url_contains("student"))
            self.assertIn("student", driver.current_url)
            print("Logout successful.")
        except Exception as e:
            print(f"Logout error: {e}")
            self.fail("Logout failed. Did not redirect to access page.")

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        # Remove the database session and drop all tables
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

if __name__ == "__main__":
    # Create a test suite and add tests in the desired order
    suite = unittest.TestSuite()
    suite.addTest(TestFlaskApp('test_register_and_login'))
    suite.addTest(TestFlaskApp('test_create_request'))
    suite.addTest(TestFlaskApp('test_find_request'))
    suite.addTest(TestFlaskApp('test_ranking_page'))
    suite.addTest(TestFlaskApp('test_login_logout'))


    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
