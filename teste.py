import pyautogui
import time
from datetime import datetime

time.sleep(5)

data = datetime.now().strftime("%d/%m/%Y")

for n in range(1):
    pyautogui.write(data, interval=0.15)
    