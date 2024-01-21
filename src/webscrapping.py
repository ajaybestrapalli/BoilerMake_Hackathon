from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
edge_options = webdriver.EdgeOptions()
edge_options.add_argument('--headless')
driver = webdriver.Edge(options=edge_options)
driver.get("https://www.purdue.edu/directory/")
search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'basicSearchInput'))
 )
search_bar.send_keys('Vaibhav Charan')
search_bar.submit()
driver.implicitly_wait(5)
error_check = driver.find_element(By.ID, "results")
if error_check.text == "Sorry, nothing matches your query.":
    print("does not exists")
else:
 search_results = driver.find_element(By.CLASS_NAME, "more")
 a = search_results.text
 stringa = a.split("EMAIL ")[1]
 stringb = stringa.split("\n")[0]
 print(stringb)
 driver.quit()
