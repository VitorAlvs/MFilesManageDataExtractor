import time
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_manage_data(driver, subscription_id, alias, username, password):
    """
    Performs data extraction of users and vaults from a subscription in Manage.
    """
    print(f"Starting extraction for subscription: {alias}")
    driver.get(config.MANAGE_BASE_URL.format(subscription_id))
    time.sleep(5)
    assert "M-Files" in driver.title
    print(f'Subscription page {alias} opened.')

    # Perform login
    usr = f'{alias}/{username}'
    driver.find_element(By.ID, "Username").send_keys(usr)
    driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click() # This is likely the "Sign In" button
    print("Login successful.")
    time.sleep(10)
    
    # Navigate to 'Vaults' and download CSV
    vaults_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/vaults')]"))
    )
    driver.execute_script("arguments[0].click();", vaults_link)
    print("Navigated to 'Vaults'.")
    time.sleep(2)
    
    print("Maximizing window")
    driver.maximize_window()
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME, "mf-icon-animatedContainer").click()
    print('Vaults CSV download initiated.')
    time.sleep(3)

    # Navigate to 'Internal users' and download CSV
    try:
        internal_users_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/users/internal')]"))
        )
        driver.execute_script("arguments[0].click();", internal_users_link)
        print("Navigated to 'Internal Users'.")
    except Exception as e:
        print(f"Did not find the users link. Attempting to open side menu: {e}")
        driver.find_element(By.XPATH, "//nav//li[contains(.,'Users')]").click() # Removed 'Usuários'
        time.sleep(2)
        internal_users_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/users/internal')]"))
        )
        driver.execute_script("arguments[0].click();", internal_users_link)

    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "export-button").click() # This is the export button
    print('Users CSV download initiated.')
    time.sleep(3)

    # Perform logout
    driver.find_element(By.CLASS_NAME, "login-menu").click()
    driver.find_element(By.ID, "logout").click()
    time.sleep(1)
    driver.find_element(By.ID, "primary-button").click()
    print(f"Logout from subscription {alias} completed.")
    time.sleep(2)