from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 启用无头模式
options.add_argument("--no-sandbox")  # 在无 GUI 环境下运行时需要
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome()
# driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
# driver = webdriver.PhantomJS(executable_path="./phantomjs")

driver.get("http://www.google.com")
print(driver.title)

driver.quit()