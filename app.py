import os
import time
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
  
  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')

# Mantém o navegador aberto após o script finalizar (útil para depuração)
options.add_experimental_option("detach", True)

prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

options.add_experimental_option("prefs", prefs)

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=options)

navegador.get('https://192.168.224.197/Cobranca/index.aspx')

# navegador.maximize_window() -- mantem a janela do navegador no tamanho padrão para evitar problemas de elementos fora da tela

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

# Dá 2 TABs para chegar no primeiro dropdown "Tipo de Relatório"
for _ in range(1):
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


# 1️⃣ Marca o checkbox (isso dispara POSTBACK)
navegador.switch_to.active_element.send_keys(Keys.SPACE)

# 2️⃣ Aguarda o postback terminar e o campo aparecer

iframes = navegador.find_elements(By.TAG_NAME, "iframe")

for i, frame in enumerate(iframes):
    navegador.switch_to.frame(frame)
    if navegador.find_elements(By.ID, "txtDtInicio"):
        print("Iframe correto:", i)
        break
    navegador.switch_to.default_content()


data_inicio = datetime.now().strftime("%d/%m/%Y")
data_fim = datetime.now().strftime("%d/%m/%Y")


navegador.execute_script("""
    function setDate(id, value) {
        const input = document.getElementById(id);
        if (!input) return;

        input.focus();
        input.click();
        input.value = '';
        input.value = value;

        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('blur', { bubbles: true }));
    }

    setDate('txtDtInicio', arguments[0]);
    setDate('txtDtFim', arguments[1]);
""", data_inicio, data_fim)


def limpar_downloads_xlsx(pasta):
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".xlsx"):
            caminho = os.path.join(pasta, arquivo)
            try:
                os.remove(caminho)
                print(f"Arquivo removido: {arquivo}")
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {e}")


botao_consultar = WebDriverWait(navegador, 30).until(
    EC.element_to_be_clickable((By.ID, "btnConsultar"))
)



navegador.execute_script("""
    document.getElementById('btnConsultar').click();
""")



def esperar_download_xlsx(pasta, timeout=40):
    inicio = time.time()
    while time.time() - inicio < timeout:
        arquivos = [
            f for f in os.listdir(pasta)
            if f.endswith(".xlsx") and not f.endswith(".crdownload")
        ]
        if arquivos:
            return os.path.join(pasta, arquivos[0])
        time.sleep(1)



arquivo_baixado = esperar_download_xlsx(DOWNLOAD_DIR)
print("Download concluído:", arquivo_baixado)

# Fecha o navegador e encerra a sessão
navegador.quit()
