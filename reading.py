from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import telebot

# Caminho .Json
with open('C:\\Users\\higor.carvalho\\Desktop\\Aviator\\config.json') as config_file:
    config = json.load(config_file)

# Configure o caminho para o ChromeDriver
service = Service(executable_path='C:\\Users\\higor.carvalho\\Desktop\\Aviator\\Selenium\\chromedriver-win32\\chromedriver.exe')

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--headless")  # Adicionando o modo headless
# chrome_options.add_argument("--start-maximized")

# Crie uma instância do navegador Chrome
browser = webdriver.Chrome(service=service, options=chrome_options)

# Dados Telegram
token = config['tokentelegram']
chat_id = config['chat_id_telegram']
bot = telebot.TeleBot(token)

iframe = '/html/body/app-root/cs-layout-casino-game/div/div[2]/div/div/casino-app-game/div/div/div/div/div/app-casino-game-item/div/div/div[2]/iframe'
Velas = '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div'

# Função para aguardar o carregamento do iframe
def switch_to_iframe(iframe_xpath):
    try:
        iframe_element = WebDriverWait(browser, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_xpath))
        )
        print("Iframe encontrado e contexto trocado com sucesso!")
    except Exception as e:
        print(f"Erro ao trocar para o iframe: {e}")
        browser.save_screenshot('iframe_error.png')

# Navegue até a página desejada
browser.get('https://br.novibet.com/cassino/jogo/nyx_aviator')
print('Página acessada com sucesso...')
sleep(2)


# Fechar a propaganda de login
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div/app-dialog/app-register-or-login/div/div[1]'))
).click()
print('Fechar propaganda de login')

# Realizar o login
try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/app-dialog/app-login/div/form/cm-input[1]/div/div[2]/input'))
    ).send_keys('higor-henrry@hotmail.com')
    print('Username preenchido com sucesso...')
    
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/app-dialog/app-login/div/form/cm-input[2]/div/div[2]/input'))
    ).send_keys('Carvalho106')
    print('Password preenchido com sucesso...')
    
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/app-dialog/app-login/div/form/cm-button/button/span'))
    ).click()
    print('Acesso concluído')

    # Fechar a propaganda de cookies
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-accept-cookies/div/div[2]/button'))
    ).click()
    print('Aceitar cookies')

    # Fechar a propaganda tutorial
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/cm-tutorial/div/div[1]/div[2]/div'))
    ).click()
    print('Fechar propaganda tutorial')

    print("Configurando iframe...")

    # Trocando para o iframe
    switch_to_iframe(iframe)

    sleep(5)
    
    # Verificar se o elemento "Velas" está presente e acessível
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, Velas))
        )
        print('Elemento "Velas" encontrado!')
    except Exception as e:
        print(f"Erro ao encontrar o elemento 'Velas': {e}")
        browser.save_screenshot('velas_error.png')

except Exception as e:
    print(f"Erro: {e}")
    browser.save_screenshot('error.png')

finally:
    browser.quit()
