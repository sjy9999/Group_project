# # Selenium测试示例
# from selenium import webdriver

# driver = webdriver.Chrome()
# driver.get("http://localhost:5000/api/data")
# element = driver.find_element_by_tag_name('body')
# assert "key" in element.text
# driver.close()




# from selenium import webdriver
# from selenium.webdriver.common.by import By

# driver = webdriver.Chrome()  # 确保已正确设置webdriver路径或已将其添加到PATH
# driver.get("http://localhost:5000")  # 将URL替换为你需要测试的页面

# # 使用新的元素查找方式
# element = driver.find_element(By.TAG_NAME, 'body')
# print(element.text)

# driver.quit()  # 关闭浏览器驱动





from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 创建 WebDriver 实例，这里以 Chrome 为例
driver = webdriver.Chrome()
warnings.filterwarnings('ignore', category=SAWarning)
try:
    # 打开登录页面
    driver.get('http://localhost/')  # 更改为你的登录URL
    
    print("启动浏览器")
    driver = webdriver.Chrome()
    print("打开网页")
    driver.get("http://localhost:5000")  # 确保这是正确的 URL
    print("查找元素")
    element = driver.find_element(By.ID, "some-id")
    print("测试完成")


    # 等待页面加载完毕
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )

    # 找到输入框并输入用户名和密码
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    # username_input.send_keys('your_username')  # 替换为你的用户名
    # password_input.send_keys('your_password')  # 替换为你的密码
    
    username_input.send_keys('andy')  # 替换为你的用户名
    password_input.send_keys('123')  # 替换为你的密码
    
    
    
    # 提交登录表单
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary[name="login"]')
    login_button.click()

    # 检查是否登录成功，可以通过查找只有在登录后才出现的页面元素来确认
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[onclick*='createRequest']"))  # 假设登录后会出现“Create Request”按钮
    )

    print("登录成功！")

    # # 继续进行其他操作，比如点击“Create Request”按钮
    # create_request_button = driver.find_element(By.CSS_SELECTOR, "button[onclick*='createRequest']")
    # create_request_button.click()
    
    

    # # 提交登录表单
    # login_button = driver.find_element(By.ID, 'login-button')  # 根据实际情况调整元素选择器
    # login_button.click()

    # # 检查是否登录成功，可以通过查找只有在登录后才出现的页面元素来确认
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, 'logout-button'))  # 假设登录后会出现注销按钮
    # )

    # print("登录成功！")

    # # 继续进行其他操作，比如访问受保护的页面
    # driver.get('http://localhost/main')

finally:
    print("启动浏览器")
    # 测试完成后关闭浏览器
    driver.quit()
