from AlphaBotV1 import AlphaBot
import time
import socket

def main():

    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('0.0.0.0',8000))
    s.listen(50)
    conn, addr = s.accept()
    conn.send(b"Connessione riuscita usa: WASD")
    print("Host Collegato: ", addr)
    Ab = AlphaBot()
    Ab.stop()

    while(1):
        data = conn.recv(1024).decode()

        if data == "exit":
            print("Connessione terminata")
            conn.close
            s.close
            break

        if data == "w":
            Ab.forward()
            time.sleep(1)
        if data == "s":
            Ab.backward()
            time.sleep(1)
        if data == "a":
            Ab.left()
            time.sleep(0.3)
        if data == "d":
            Ab.right()
            time.sleep(0.3)
    
        Ab.stop()
        

if __name__ =="__main__":
    main()

