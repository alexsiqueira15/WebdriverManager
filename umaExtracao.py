import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import threading
import time
import os
import calendar
import pandas as pd

from datetime import datetime

URL = "https://192.168.224.197/Cobranca/index.aspx"


class Sistema:

    def __init__(self, root):

        self.root = root
        self.root.title("Sistema de Cobrança")
        self.root.geometry("700x520")
        self.root.resizable(False, False)

        self.executando = False

        self.caminho_driver = tk.StringVar(
            value="C:\\Users\\ADM - SICOL\\Pagow Aju\\Serverdados - Documentos\\Sicol\\Alex Santos\\webdriver\\msedgedriver.exe"
        )

        self.pasta_download = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "C:\\Users\\ADM - SICOL\\Pagow Aju\\Serverdados - Documentos\\Sicol\\Alex Santos\\webdriver\\downloads")
        )

        self.usuario = tk.StringVar(value="4059468")
        self.senha = tk.StringVar(value="134679")

        
        self.intervalo_execucao = tk.IntVar(value=10)

        # ==========================================================
        # DRIVER
        # ==========================================================

        tk.Label(
            root,
            text="Intervalo (minutos):",
            font=("Arial", 10)
        ).pack(pady=(15, 5))
        
        self.entry_intervalo = tk.Entry(
            root,
            textvariable=self.intervalo_execucao,
            width=10,
            justify="center"
        )
        self.entry_intervalo.pack()

        tk.Label(
            root,
            text="Caminho do msedgedriver.exe:",
            font=("Arial", 10)
        ).pack(pady=(15, 5))
        


        frame_driver = tk.Frame(root)
        frame_driver.pack()

        self.entry_driver = tk.Entry(
            frame_driver,
            textvariable=self.caminho_driver,
            width=60
        )

        self.entry_driver.pack(side=tk.LEFT, padx=5)

        self.btn_driver = tk.Button(
            frame_driver,
            text="Procurar",
            command=self.selecionar_driver
        )

        self.btn_driver.pack(side=tk.LEFT)

        # ==========================================================
        # PASTA DOWNLOAD
        # ==========================================================

        tk.Label(
            root,
            text="Pasta para salvar downloads:",
            font=("Arial", 10)
        ).pack(pady=(15, 5))

        frame_pasta = tk.Frame(root)
        frame_pasta.pack()

        self.entry_pasta = tk.Entry(
            frame_pasta,
            textvariable=self.pasta_download,
            width=60
        )

        self.entry_pasta.pack(side=tk.LEFT, padx=5)

        self.btn_pasta = tk.Button(
            frame_pasta,
            text="Selecionar",
            command=self.selecionar_pasta
        )

        self.btn_pasta.pack(side=tk.LEFT)

        # ==========================================================
        # USUÁRIO
        # ==========================================================

        tk.Label(
            root,
            text="Usuário:",
            font=("Arial", 10)
        ).pack(pady=(15, 5))

        self.entry_usuario = tk.Entry(
            root,
            textvariable=self.usuario,
            width=35
        )

        self.entry_usuario.pack()

        # ==========================================================
        # SENHA
        # ==========================================================

        tk.Label(
            root,
            text="Senha:",
            font=("Arial", 10)
        ).pack(pady=(15, 5))

        self.entry_senha = tk.Entry(
            root,
            textvariable=self.senha,
            show="*",
            width=35
        )

        self.entry_senha.pack()

        # ==========================================================
        # HORÁRIO
        # ==========================================================



        # ==========================================================
        # BOTÃO
        # ==========================================================

        self.btn_iniciar = tk.Button(
            root,
            text="Iniciar Sistema",
            bg="#2E8B57",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            command=self.iniciar_sistema
        )

        self.btn_iniciar.pack(pady=25)

        # ==========================================================
        # LOG
        # ==========================================================

        self.text_log = tk.Text(
            root,
            height=10,
            width=82
        )

        self.text_log.pack(pady=10)

    # ==========================================================
    # LOG
    # ==========================================================

    def log(self, mensagem):

        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.text_log.insert(
            tk.END,
            f"[{horario}] {mensagem}\n"
        )

        self.text_log.see(tk.END)

    # ==========================================================
    # BLOQUEAR CAMPOS
    # ==========================================================

    def bloquear_campos(self):

        self.entry_driver.config(state="disabled")
        self.entry_pasta.config(state="disabled")
        self.entry_usuario.config(state="disabled")
        self.entry_senha.config(state="disabled")

        self.btn_driver.config(state="disabled")
        self.btn_pasta.config(state="disabled")

        self.btn_iniciar.config(
            state="disabled",
            text="Sistema Rodando..."
        )

    # ==========================================================
    # SELECIONAR DRIVER
    # ==========================================================

    def selecionar_driver(self):

        caminho = filedialog.askopenfilename(
            title="Selecione o msedgedriver.exe",
            filetypes=[("Edge Driver", "msedgedriver.exe")]
        )

        if caminho:
            self.caminho_driver.set(caminho)

    # ==========================================================
    # SELECIONAR PASTA
    # ==========================================================

    def selecionar_pasta(self):

        pasta = filedialog.askdirectory(
            title="Selecione a pasta de download"
        )

        if pasta:
            self.pasta_download.set(pasta)

    # ==========================================================
    # LIMPAR PASTA
    # ==========================================================

    def limpar_pasta_download(self):

        pasta = self.pasta_download.get()

        for arquivo in os.listdir(pasta):

            caminho = os.path.join(pasta, arquivo)

            try:

                if os.path.isfile(caminho):
                    os.remove(caminho)

            except:
                pass

    # ==========================================================
    # INICIAR
    # ==========================================================

    def iniciar_sistema(self):

        if not self.senha.get():

            messagebox.showerror(
                "Erro",
                "Informe a senha!"
            )

            return

        self.executando = True

        self.bloquear_campos()

        self.log(
            f"Sistema iniciado. Execução diária a cada {self.intervalo_execucao.get()} minutos."
        )

        threading.Thread(
            target=self.loop_agendamento,
            daemon=True
        ).start()

    # ==========================================================
    # LOOP INFINITO
    # ==========================================================

    def loop_agendamento(self):
        
        while self.executando:
            
            self.log("Executando extração...")
            
            try:

                self.executar_fluxo()

                self.log("Extração finalizada com sucesso.")
                
            except Exception as e:

                self.log(f"Erro: {str(e)}")
            
            intervalo = self.intervalo_execucao.get() * 60
            
            self.log(f"Aguardando {self.intervalo_execucao.get()} minutos...")
            
            time.sleep(intervalo)

    '''def loop_agendamento(self):

        ultima_execucao = None

        while self.executando:

            agora = datetime.now().strftime("%H:%M")
            hoje = datetime.now().strftime("%Y-%m-%d")

            horario_programado = self.horario_execucao.get()

            chave_execucao = f"{hoje}_{horario_programado}"

            if agora == horario_programado:

                if ultima_execucao != chave_execucao:

                    ultima_execucao = chave_execucao

                    self.log("Horário atingido. Executando script...")

                    try:

                        self.executar_fluxo()

                        self.log("Execução finalizada com sucesso.")

                    except Exception as e:

                        self.log(f"Erro: {str(e)}")

            time.sleep(20)'''

    # ==========================================================
    # EXECUTAR FLUXO
    # ==========================================================

    def executar_fluxo(self):

        driver = None

        try:

            service = Service(self.caminho_driver.get())

            options = Options()

            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--start-maximized")

            prefs = {
                "download.default_directory": os.path.abspath(
                    self.pasta_download.get()
                ),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }

            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Edge(
                service=service,
                options=options
            )

            wait = WebDriverWait(driver, 30)

            self.log("Abrindo sistema...")

            driver.get(URL)

            # LOGIN

            wait.until(
                EC.presence_of_element_located(
                    (By.ID, "txtUsuarioLogin")
                )
            ).send_keys(self.usuario.get())

            driver.find_element(
                By.ID,
                "txtSenhaLogin"
            ).send_keys(self.senha.get())

            driver.find_element(
                By.ID,
                "btnOkLogin"
            ).click()

            self.log("Login realizado.")

            # MENU

            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//td[contains(text(),'Consulta')]")
                )
            ).click()

            wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "tdMenu1_SolpartMenu10306")
                )
            ).click()

            time.sleep(2)

            # IFRAME

            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            if iframes:
                driver.switch_to.frame(iframes[0])

            # RELATÓRIO

            select_relatorio = wait.until(
                EC.presence_of_element_located(
                    (By.ID, "ddlConsulta")
                )
            )

            Select(select_relatorio).select_by_value("194")

            time.sleep(3)

            self.log("Relatório 194 selecionado.")

            # EXCEL

            try:

                wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, "rbExcel")
                    )
                ).click()

            except:
                pass

            # PERÍODO

            try:

                chk_periodo = wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, "chkPeriodo")
                    )
                )

                if not chk_periodo.is_selected():
                    chk_periodo.click()

            except:
                pass

            # DATAS
            data_inicio = datetime.now().strftime("%d/%m/%Y")
            data_fim = datetime.now().strftime("%d/%m/%Y")

            campo_inicio = wait.until(
                EC.presence_of_element_located(
                    (By.ID, "txtDtInicio")
                )
            )

            campo_inicio.clear()
            campo_inicio.send_keys(data_inicio)
            campo_inicio.send_keys(Keys.TAB)

            time.sleep(1)

            campo_final = driver.switch_to.active_element

            campo_final.clear()
            campo_final.send_keys(data_fim)

            # LIMPAR PASTA

            self.limpar_pasta_download()

            arquivos_antes = set(
                os.listdir(self.pasta_download.get())
            )

            # CONSULTAR

            wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "btnConsultar")
                )
            ).click()

            self.log("Aguardando download...")

            arquivo_baixado = None

            for _ in range(60):

                time.sleep(1)

                arquivos_depois = set(
                    os.listdir(self.pasta_download.get())
                )

                novos_arquivos = arquivos_depois - arquivos_antes

                arquivos_validos = [
                    arq for arq in novos_arquivos
                    if not arq.endswith(".crdownload")
                    and not arq.endswith(".tmp")
                ]

                if arquivos_validos:

                    arquivo_baixado = arquivos_validos[0]
                    break

            if not arquivo_baixado:

                self.log("Download não encontrado.")
                return

            caminho_arquivo = os.path.join(
                self.pasta_download.get(),
                arquivo_baixado
            )

            self.log(f"Arquivo baixado: {arquivo_baixado}")

            # CONVERTER

            tabelas = pd.read_html(caminho_arquivo)

            df = tabelas[0]

            nome_csv = os.path.splitext(
                arquivo_baixado
            )[0] + ".csv"

            caminho_csv = os.path.join(
                self.pasta_download.get(),
                nome_csv
            )

            df.to_csv(
                caminho_csv,
                index=False,
                encoding="utf-8-sig",
                sep=";"
            )

            self.log(f"CSV gerado: {caminho_csv}")

        except Exception as e:

            self.log(f"Erro: {str(e)}")

        finally:

            if driver:
                driver.quit()

            self.log("Driver finalizado.")


if __name__ == "__main__":

    root = tk.Tk()

    app = Sistema(root)

    root.mainloop()