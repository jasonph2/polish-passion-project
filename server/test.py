from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# path = "C:\Program Files (x86)\chromedriver.exe"
service = webdriver.ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://dictionary.cambridge.org/us/dictionary/polish-english/w")
driver.close()