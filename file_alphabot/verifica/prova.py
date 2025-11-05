# prova: farlo fermare ogni volta per essere più preciso
from AlphaBotV2 import AlphaBot
import time

Ab = AlphaBot()
Ab.stop()

for i in range(9):
    Ab.forward(0.5)
    print(i)
    time.sleep(2)
