import time
import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



    
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=options)

navegador.get('https://192.168.224.197/Cobranca/index.aspx')

wait = WebDriverWait(navegador, 10)

# Login
usuario = wait.until(EC.presence_of_element_located((By.ID, "txtUsuarioLogin")))
usuario.clear()
usuario.send_keys("4059468")

senha = navegador.find_element(By.ID, "txtSenhaLogin")
senha.clear()
senha.send_keys("134679")

botao = navegador.find_element(By.ID, "btnOkLogin")
botao.click()

# Menu "Consulta"
consulta = wait.until(EC.presence_of_element_located((By.ID, "tdMenu1_SolpartMenu103")))

# Hover (importante nesses menus antigos)
ActionChains(navegador).move_to_element(consulta).perform()

# Clique forçado
navegador.execute_script("arguments[0].click();", consulta)

# Submenu
submenu = wait.until(EC.presence_of_element_located((By.ID, "iconMenu1_SolpartMenu10306")))
navegador.execute_script("arguments[0].click();", submenu)

# Garante que algo da página está focado
body = navegador.find_element(By.TAG_NAME, "body")
body.click()

# Dá 2 TABs
for _ in range(2):
    navegador.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(0.2)  # pequeno delay ajuda estabilidade

# Seta para direita para marcar "Excel"
navegador.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)

# Dá mais 5 TABs para chegar no campo do relatório
for _ in range(5):
    navegador.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(0.2)  # pequeno delay ajuda estabilidade

# Digita o código 194 no campo focado
navegador.switch_to.active_element.send_keys("194")

# Dá mais 6 TABs para chegar no checkbox "Períodos"
for _ in range(6):
    navegador.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(0.2) 
    
navegador.switch_to.active_element.send_keys(Keys.SPACE)

# Dá mais 7 TABs para chegar no campo de datas
for _ in range(7):
    navegador.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(0.2)    

# espera o campo existir após o postback
campo = WebDriverWait(navegador, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='txtDtInicio']"))
)

campo.click()
# pequena pausa
time.sleep(1)
data = datetime.now().strftime("%d%m%Y")
# digita REAL no teclado
pyautogui.write(data, interval=0.15)

input()