import pytest
from flask import url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # 设置测试环境
    flask_app.config.from_object('config.TestingConfig')

    testing_client = flask_app.test_client()

    # 建立应用上下文
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # 这个是测试运行的地方

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    # 插入测试数据
    user1 = User(name='testuser1', email='testuser1@example.com')
    user1.set_password('Password1')
    db.session.add(user1)
    db.session.commit()

    yield db

    db.drop_all()

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_register(test_client, init_database):
    response = test_client.post('/register', data=dict(
        username='newuser',
        email='newuser@example.com',
        password='Password1'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"success" in response.data

def test_login(test_client, init_database):
    response = test_client.post('/login', data=dict(
        username='testuser1',
        password='Password1'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"Login successful!" in response.data

def test_dashboard_access(test_client, init_database):
    response = test_client.post('/login', data=dict(
        username='testuser1',
        password='Password1'
    ), follow_redirects=True)

    assert response.status_code == 200

    response = test_client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data

@pytest.fixture(scope='module')
def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_register_with_selenium(selenium_driver):
    selenium_driver.get("http://127.0.0.1:5000/register")
    username_input = selenium_driver.find_element(By.NAME, "username")
    email_input = selenium_driver.find_element(By.NAME, "email")
    password_input = selenium_driver.find_element(By.NAME, "password")

    username_input.send_keys("seleniumuser")
    email_input.send_keys("seleniumuser@example.com")
    password_input.send_keys("Password1")
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(selenium_driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "success")
    )

def test_login_with_selenium(selenium_driver):
    selenium_driver.get("http://127.0.0.1:5000/login")
    username_input = selenium_driver.find_element(By.NAME, "username")
    password_input = selenium_driver.find_element(By.NAME, "password")

    username_input.send_keys("seleniumuser")
    password_input.send_keys("Password1")
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(selenium_driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Login successful!")
    )

def test_dashboard_with_selenium(selenium_driver):
    selenium_driver.get("http://127.0.0.1:5000/login")
    username_input = selenium_driver.find_element(By.NAME, "username")
    password_input = selenium_driver.find_element(By.NAME, "password")

    username_input.send_keys("seleniumuser")
    password_input.send_keys("Password1")
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(selenium_driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Login successful!")
    )

    selenium_driver.get("http://127.0.0.1:5000/dashboard")
    WebDriverWait(selenium_driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Dashboard")
    )
