from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=options)

navegador.get('https://192.168.224.197/Cobranca/index.aspx')
input()

# 👉 Ajuste esses IDs conforme sua página
usuario = navegador.find_element(By.ID, "txtUsuarioLogin")
senha = navegador.find_element(By.ID, "txtSenhaLogin")
botao = navegador.find_element(By.ID, "btnOKLogin")

# Preenche
usuario.send_keys("4059468")
senha.send_keys("134679")

# Clica
botao.click()

input()