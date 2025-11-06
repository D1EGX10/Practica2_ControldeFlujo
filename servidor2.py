import socket
import time
import random

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5500
WINDOW_SIZE = 5
PACKET_SIZE = 1024
LOSS_PROBABILITY = 0.05  

def servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Servidor UDP escuchando en {SERVER_IP}:{SERVER_PORT}")

    data, addr = sock.recvfrom(1024)
    if data.decode() != "Solicito cancion":
        print("Solicitud inválida.")
        return

    print("Solicitud recibida. Iniciando envío...")

   
    with open("SMB.mp3", "rb") as f:
        partes = []
        i = 0
        while chunk := f.read(PACKET_SIZE):
            partes.append(f"{i}|".encode() + chunk)
            i += 1

    total_paquetes = len(partes)
    print(f"Total de paquetes: {total_paquetes}")

    base = 0
    next_seq = 0
    ultimo_ack = -1
    sock.settimeout(2)

    while base < total_paquetes:
       
        while next_seq < base + WINDOW_SIZE and next_seq < total_paquetes:
            if random.random() > LOSS_PROBABILITY:
                sock.sendto(partes[next_seq], addr)
                print(f"Enviado paquete {next_seq}")
            else:
                print(f"Paquete {next_seq} perdido (simulado)")
            next_seq += 1

        try:
            data, _ = sock.recvfrom(1024)
            if data.startswith(b"ACK|"):
                ack_num = int(data.decode().split("|")[1])
                print(f"ACK recibido: {ack_num}")

                if ack_num >= base:
                    base = ack_num + 1
                    ultimo_ack = ack_num

        except socket.timeout:
            print("Timeout: reenviando desde el último ACK confirmado...")
            
            next_seq = base

        time.sleep(0.05)

    sock.sendto(b"FIN", addr)
    print("Transmisión finalizada correctamente.")

if __name__ == "__main__":
    servidor()






