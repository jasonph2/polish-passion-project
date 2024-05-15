from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

service = webdriver.ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls = [
    "https://dictionary.cambridge.org/us/dictionary/polish-english/i",
    "https://dictionary.cambridge.org/us/dictionary/polish-english/w",
]

xpath = '/html/body/div[2]/div/div[1]/div[2]/article/div[2]/div[1]/span/div/div[4]/div/div[1]/div[2]/div/div[3]/span/a/span'

try:
    for url in urls:
        driver.get(url)
        try:
            element = driver.find_element("xpath", xpath)
            print(f"Element Text from {url}:", element.text)
        except Exception as e:
            print(f"An error occurred on {url}: {e}")

except Exception as e:
    print(f"An overall error occurred: {e}")

# Close the browser
driver.quit()