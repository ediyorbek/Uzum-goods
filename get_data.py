from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

url = "https://uzum.uz"
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(5)

all_products = []

while True:
    try:
        product_containers = driver.find_elements(By.CSS_SELECTOR, "div[class='ui-card']")
        
        for product in product_containers:
            new_clean_price = None
            clean_name = None
            rate_text = None
            clean_feedback = None
            old_clean_price = None

            price_elements = product.find_elements(By.CSS_SELECTOR, "span[data-test-id='text__price']")
            if price_elements:
                new_clean_price = price_elements[0].text.replace("&nbsp;", "").replace("сум", "").strip()

            name_elements = product.find_elements(By.CSS_SELECTOR, "div[data-test-id='text__product-name']")
            if name_elements:
                clean_name = name_elements[0].text.replace(",", "").replace('"', "").replace("'", "").strip()

            rate_elements = product.find_elements(By.CSS_SELECTOR, "span[data-test-id='text__rating']")
            if rate_elements:
                rate_text = rate_elements[0].text
            else:
                novelty_elements = product.find_elements(By.CSS_SELECTOR, "span[data-test-id='text__status-novelty']")
                if novelty_elements:
                    rate_text = novelty_elements[0].text

            feedback_elements = product.find_elements(By.CSS_SELECTOR, "span[class='orders__feedback-amount']")
            if feedback_elements:
                clean_feedback = feedback_elements[0].text.replace("(", "").replace(")", "").replace("отзыв", "").replace("а", "").replace("ов", "").strip()

            old_price_elements = product.find_elements(By.CSS_SELECTOR, "span[data-test-id='text__old-price']")
            if old_price_elements:
                old_clean_price = old_price_elements[0].text.replace("&nbsp;", "").strip()

            product_data = {
                "name": clean_name,
                "new_price": new_clean_price,
                "old_price": old_clean_price,
                "rate": rate_text,
                "feedback": clean_feedback,
            }
            all_products.append(product_data)

        next_button = driver.find_elements(By.CSS_SELECTOR, "button[class*='next-page']")
        if next_button and next_button[0].is_enabled():
            next_button[0].click()
            driver.implicitly_wait(5)
        else:
            break

    except Exception as e:
        print(f"Ошибка при обработке страницы: {e}")
        break

df = pd.DataFrame(all_products)
df.to_csv("products.csv", index=False)

driver.quit()