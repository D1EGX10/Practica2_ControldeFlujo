import socket
import time
from playsound import playsound

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5500

def cliente():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Solicito cancion", (SERVER_IP, SERVER_PORT))

    recibido = {}
    inicio = time.time()

    print("Esperando datos...")

    while True:
        data, _ = sock.recvfrom(2048)

        if data == b"FIN":
            print("Transmisión completa.")
            break

        try:
            partes = data.split(b"|", 1)
            seq = int(partes[0])
            fragmento = partes[1]
        except Exception:
            continue

        if seq not in recibido:
            recibido[seq] = fragmento
            if seq % 100 == 0:
                print(f"Recibido paquete {seq}")

        ack = f"ACK|{seq}".encode()
        sock.sendto(ack, (SERVER_IP, SERVER_PORT))

    fin = time.time()
    print(f"Tiempo total: {fin - inicio:.2f} segundos")
    print(f"Total paquetes recibidos: {len(recibido)}")

    total = max(recibido.keys()) + 1
    faltantes = [i for i in range(total) if i not in recibido]
    if faltantes:
        print(f"Faltan {len(faltantes)} paquetes.")

    with open("recibido.mp3", "wb") as f:
        for i in range(total):
            if i in recibido:
                f.write(recibido[i])
            else:
                f.write(b"\x00" * 1024)

    print("Archivo reconstruido como 'recibido.mp3'")

    try:
        print("Reproduciendo canción...")
        playsound("recibido.mp3")
    except Exception as e:
        print("No se pudo reproducir automáticamente:", e)

if __name__ == "__main__":
    cliente()





