import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('192.168.1.109', 7000))
    resp = client.recv(1024)
    print(resp.decode())

    while 1:
        if not resp:
            print("Connessione chiusa dal server")
            break

        msg = input('Inserisi comando: ')
        client.send(msg.encode())

        if msg == 'exit':
            return
    
    client.close()


if __name__ == '__main__':
    main()