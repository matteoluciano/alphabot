# tramite una soket si decide quale forma fare
from AlphaBotV1 import AlphaBot
import time
import socket

def square(Ab):

    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.28)
    Ab.stop()

    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.28)
    Ab.stop()

    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.28)
    Ab.stop()

    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.28)
    Ab.stop()


def circle(Ab):
    pass
def triangle(Ab):
    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.15)
    Ab.stop()

    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.15)
    Ab.stop()

    Ab.forward()
    time.sleep(2)
    Ab.stop()

    Ab.right()
    time.sleep(0.15)
    Ab.stop()

def main():

    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('0.0.0.0',8000))
    s.listen(50)
    conn, addr = s.accept()
    conn.send(b"Connessione riuscita usa: WASD")
    print("Host collegato: ", addr)
    Ab = AlphaBot()
    Ab.stop()

    while(1):
        data = conn.recv(1024).decode()

        if data == "exit":
            print("Connessione terminata")
            conn.close
            s.close
            break

        if data=="square":
            square()

        if data=="circle":
            circle()

        if data=="triangle":
            triangle()

if __name__ =="__main__":
    main()
