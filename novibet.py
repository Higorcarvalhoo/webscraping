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
url = config['urlnovibet']
classCandle = config['accessPaths']['classCandleNovibet'] 

def alert(lista):
    for numero in lista[:2]:
        if numero >=2:
            return False
    return True

def enter(lista):
    for numero in lista[:3]:
        if numero >=2:
            return False
    return True

def greenRed(lista):
    for numero in lista[:1]:
        if numero >= 1.5:
            bot.send_message(chat_id,'*✅✅✅ VITÓRIA ✅✅✅*', parse_mode='Markdown')
        else:
            bot.send_message(chat_id,'*❌RED❌*', parse_mode='Markdown')
            sleep(5)
            bot.send_message(chat_id,'*⏰AGUARDAR PROXIMA RODADA⏰*', parse_mode='Markdown')
            sleep(120)
            break
        break



browser.get(url)
print('Página acessada com sucesso...')
sleep(10)


try:
    while True:
        result = [float(n) for n in browser.find_element(
            By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
        while True:
            verification = [float(n) for n in browser.find_element(
                By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
            if verification != result:
                print(verification)
                if alert(verification):
                    bot.send_message(chat_id,'*⚠️ POSSIVEL ENTRADA ⚠️*', parse_mode='Markdown')
                    while True:
                        verification1 = [float(n) for n in browser.find_element(
                            By.XPATH, classCandle).text.replace('x', '').split('\n')][:10]
                        if verification1 != verification:
                            print(verification1)
                            if enter(verification1):
                                bot.send_message(chat_id,'*🛫 REALIZAR ENTRADA 🛬*', parse_mode='Markdown')
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
