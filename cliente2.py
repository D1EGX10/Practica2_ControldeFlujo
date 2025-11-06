import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5500

def cliente():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Solicito cancion", (SERVER_IP, SERVER_PORT))

    recibido = {}
    esperado = 0

    while True:
        data, _ = sock.recvfrom(2048)

        if data == b"FIN":
            print("Transmisión completa.")
            break

        partes = data.split(b"|", 1)
        seq = int(partes[0])
        fragmento = partes[1]

        recibido[seq] = fragmento
        print(f"Recibido paquete {seq}")

        ack = f"ACK|{seq}".encode()
        sock.sendto(ack, (SERVER_IP, SERVER_PORT))

    with open("recibido.mp3", "wb") as f:
        for i in range(len(recibido)):
            f.write(recibido[i])

    print("Archivo reconstruido como 'recibido.mp3'.")

if __name__ == "__main__":
    cliente()


