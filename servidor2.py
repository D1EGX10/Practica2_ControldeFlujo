import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5500
WINDOW_SIZE = 5  # Tamaño de la ventana deslizante
PACKET_SIZE = 1024

def servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor UDP escuchando en {SERVER_IP}:{SERVER_PORT}")

    data, addr = sock.recvfrom(1024)
    if data.decode() == "Solicito cancion":
        print("Solicitud de canción recibida. Iniciando envío...")

        with open("SMB.mp3", "rb") as f:
            partes = []
            i = 0
            while chunk := f.read(PACKET_SIZE):
                partes.append(f"{i}|".encode() + chunk)
                i += 1

        total_paquetes = len(partes)
        print(f"Total de paquetes: {total_paquetes}")

        base = 0
        while base < total_paquetes:
            for i in range(base, min(base + WINDOW_SIZE, total_paquetes)):
                sock.sendto(partes[i], addr)
                print(f"Enviado paquete {i}")

            sock.settimeout(2)
            try:
                data, _ = sock.recvfrom(1024)
                if data.startswith(b"ACK|"):
                    ack_num = int(data.decode().split("|")[1])
                    base = ack_num + 1
                    print(f"ACK recibido: {ack_num}")
            except socket.timeout:
                print("Tiempo de espera excedido. Reenviando ventana...")
            time.sleep(0.05)

        sock.sendto(b"FIN", addr)
        print("Transmisión finalizada.")

if __name__ == "__main__":
    servidor()


