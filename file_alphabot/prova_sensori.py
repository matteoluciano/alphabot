from AlphaBotV2 import AlphaBot
import time

Ab = AlphaBot()
Ab.stop()

Ab.forward(5)

"""
while True:



    left = Ab.left_sensor()
    rigth = Ab.right_sensor()

    if(left):
        print("Sensore letto, valore sinistro: ", left)
    if(rigth):
        print("Sensore letto, valore destro: ", rigth)"""