import pyautogui
import time

print("Você tem 5 segundos...")
time.sleep(5)

pyautogui.write("Teste PyAutoGUI funcionando", interval=0.1)