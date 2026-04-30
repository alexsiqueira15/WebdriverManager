from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=options)

navegador.get('https://192.168.224.197/Cobranca/index.aspx')

wait = WebDriverWait(navegador, 10)

# Campo usuário (matrícula)
usuario = wait.until(
    EC.presence_of_element_located((By.ID, "txtUsuarioLogin"))
)
usuario.clear()
usuario.send_keys("4059468")

# Campo senha
senha = navegador.find_element(By.ID, "txtSenhaLogin")
senha.clear()
senha.send_keys("134679")

# Botão OK
botao = navegador.find_element(By.ID, "btnOkLogin")
botao.click()

# Aguarda o menu "Consulta"
consulta = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.ID, "tdMenu1_SolpartMenu103"))
)

consulta.click()

# Aguarda o submenu aparecer e clica
submenu = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.ID, "iconMenu1_SolpartMenu10306"))
)
submenu.click()

# Aguarda o radio aparecer e clica
excel = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.ID, "rbExcel"))
)

excel.click()

input()