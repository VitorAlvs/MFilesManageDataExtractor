import time
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_dados_manage(driver, subscription_id, alias, username, password):
    """
    Realiza a extração dos dados de usuários e vaults de uma subscription no Manage.
    """
    print(f"Iniciando extração para a assinatura: {alias}")
    driver.get(config.MANAGE_BASE_URL.format(subscription_id))
    time.sleep(5)
    assert "M-Files" in driver.title
    print(f'Página da assinatura {alias} aberta.')

    # Realiza login
    usr = f'{alias}/{username}'
    driver.find_element(By.ID, "Username").send_keys(usr)
    driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/form/fieldset/div[5]/button").click()
    print("Login realizado com sucesso.")
    time.sleep(10)
    
    # Navega até 'Vaults' e faz download do CSV
    vaults_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div[1]/div/div[1]/div/div/nav/ul/li[2]/button'))
    )
    driver.execute_script("arguments[0].click();", vaults_link)
    print("Navegou para 'Vaults'.")
    time.sleep(2)
    
    print("Maximizando a janela")
    driver.maximize_window()
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME, "vault-export__label").click()
    print('Download do CSV de vaults iniciado.')
    time.sleep(3)

    # Navega até 'Internal users' e faz download do CSV
    try:
        internal_users_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div[1]/div/div[1]/div/div/nav/ul/li[3]/ul/li[1]/button'))
        )
        driver.execute_script("arguments[0].click();", internal_users_link)
        print("Navegou para 'Internal Users'.")
    except Exception as e:
        print(f"Não encontrou o link de usuários. Tentando abrir menu lateral: {e}")
        driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/div/div[1]/div/div/nav/ul/li[3]/button').click()
        time.sleep(2)
        internal_users_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div[1]/div/div[1]/div/div/nav/ul/li[3]/ul/li[1]/button'))
        )
        driver.execute_script("arguments[0].click();", internal_users_link)

    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "export-button").click()
    print('Download do CSV de usuários iniciado.')
    time.sleep(3)

    # Realiza logout
    driver.find_element(By.CLASS_NAME, "login-menu").click()
    driver.find_element(By.ID, "logout").click()
    time.sleep(1)
    driver.find_element(By.ID, "primary-button").click()
    print(f"Logout da assinatura {alias} realizado.")
    time.sleep(2)