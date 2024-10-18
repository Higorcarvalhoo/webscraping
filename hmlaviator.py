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
#chrome_options.add_argument("--headless")  # Adicionando o modo headless
chrome_options.add_argument("--start-maximized")  

# Crie uma instância do navegador Chrome
browser = webdriver.Chrome(service=service, options=chrome_options)

# Dados Telegram

token = config['tokentelegram']
chat_id = config['chat_id_telegram']
bot = telebot.TeleBot(token)

# Dados de acesso
Username = config['username']
Password = config['password']
url = config['url']
accessPathUsers = config['accessPaths']['username']
accessPathPassword = config['accessPaths']['password']
loginButton = config['accessPaths']['loginButton']
accessIframe = config['accessPaths']['accessIframe']
classCandle = config['accessPaths']['classCandle']  


def alert(lista):
    for numero in lista[:1]:
        if numero >=2:
            return False
    return True

def enter(lista):
    for numero in lista[:2]:
        if numero >=2:
            return False
    return True

def greenRed(lista):
    for numero in lista[:1]:
        if numero >= 1.5:
            print('green')
            bot.send_message(chat_id,'green')
        else:
            print('red')
            bot.send_message(chat_id,'red')
            sleep(5)
            print('Aguarde a proxima rodada...')
            bot.send_message(chat_id,'Aguarde a proxima rodada...')
            sleep(120)
            break
        break


# Navegue até a página desejada
browser.get(url)
print('Página acessada com sucesso...')

try:
    # Preencha o campo de entrada para o nome de usuário
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, accessPathUsers))
    ).send_keys(Username)
    print('Username preenchido com sucesso...')
    
    # Preencha o campo de entrada para a senha
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, accessPathPassword))
    ).send_keys(Password)
    print('Password preenchido com sucesso...')
    
    # Clique no botão de login
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, loginButton))
    ).click()
    print('Acesso concluído')

    print("Configurando iframe...")
    sleep(10)

    # Aguardando e mudando para o iframe
    WebDriverWait(browser, 40).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, accessIframe))
    )
    print("Realizada troca de Iframe...")
    sleep(5)
    

    while True:
        result = [float(n) for n in browser.find_element(
            By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
        while True:
            verification = [float(n) for n in browser.find_element(
                By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
            if verification != result:
                print(verification)
                if alert(verification):
                    print('Possivel entrada...')
                    bot.send_message(chat_id,'Possivel entrada...')
                    while True:
                        verification1 = [float(n) for n in browser.find_element(
                            By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
                        if verification1 != verification:
                            print(verification1)
                            if enter(verification1):
                                print('Realizar Entrada...')
                                bot.send_message(chat_id,'Realizar Entrada...')
                                while True:
                                    inputResult = [float(n) for n in browser.find_element(
                                By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
                                    if inputResult != verification1:
                                        print(inputResult)
                                        if greenRed(inputResult):
                                            break
                                        break
                            break 
                break
                                     
except Exception as e:
    print(f"Erro: {e}")
    browser.save_screenshot('error.png')

finally:
    browser.quit()