from AlphaBotV2 import AlphaBot
import time

Ab = AlphaBot()
Ab.stop()

Ab.setPWMA(33.2) #S
Ab.setPWMB(33) #D

Ab.forward(7)
time.sleep(1)

Ab.left(6)
time.sleep(0.45)
Ab.stop()
time.sleep(1)

Ab.setPWMA(33) #S
Ab.setPWMB(33) #D

time.sleep(1)

Ab.forward(11)
time.sleep(1)

#Ab.left()
#time.sleep(0.4)
#Ab.stop()
#time.sleep(1)
""""
Ab.setPWMA(31) #S
Ab.setPWMB(30) #D

time.sleep(0.5)
Ab.forward(5)

Ab.setPWMA(32) #S
Ab.setPWMB(31) #D

time.sleep(0.5)
Ab.forward(4)
time.sleep(1)

Ab.left()
time.sleep(0.35)

Ab.setPWMA(30)
Ab.setPWMB(30)

time.sleep(0.75)
Ab.forward(4)"""
   
""" if left and right:
        Ab.stop()
        time.sleep(0.3)
        Ab.backward()
        time.sleep(1.0)
        Ab.stop()
        time.sleep(0.3)
        Ab.right()
        time.sleep(0.6)
        Ab.stop()
        time.sleep(0.3)

    elif left and not right:
        Ab.stop()
        time.sleep(0.15)
        Ab.right()
        time.sleep(0.4)
        Ab.stop()
        time.sleep(0.15)

    elif right and not left:
        Ab.stop()
        time.sleep(0.15)
        Ab.left()
        time.sleep(0.3)
        Ab.stop()
        time.sleep(0.15)

"""
