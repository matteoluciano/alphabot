from AlphaBotV1 import AlphaBot
import time

Ab = AlphaBot()
Ab.stop()

while True:

    Ab.forward()
    left = Ab.left_sensor()
    rigth = Ab.right_sensor()

    if(left & rigth):
        print("Entrambi sensori letti")
        Ab.stop()
        time.sleep(0.5)

        Ab.backward()
        time.sleep(1)
        Ab.stop()
        time.sleep(1)

        Ab.right()
        time.sleep(0.28)
        Ab.stop()
        time.sleep(0.5)

    elif(rigth):
        print("Sensore destro letto")
        Ab.stop()
        time.sleep(0.5)

        Ab.backward()
        time.sleep(0.5)
        Ab.stop()
        time.sleep(0.5)

        Ab.left()
        time.sleep(0.20)
        Ab.stop()
        time.sleep(0.5)
        
    elif(left):
        print("Sensore sinistro letto")
        Ab.stop()
        time.sleep(0.5)

        Ab.backward()
        time.sleep(0.5)
        Ab.stop()
        time.sleep(0.5)

        Ab.right()
        time.sleep(0.20)
        Ab.stop()
        time.sleep(0.5)