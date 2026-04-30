from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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



input("Finalizado. Pressione Enter para sair...")