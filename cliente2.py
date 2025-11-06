import socket
import time
from playsound import playsound

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5500

def cliente():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Solicito cancion", (SERVER_IP, SERVER_PORT))

    recibido = {}
    esperado = 0
    inicio = time.time()

    while True:
        data, _ = sock.recvfrom(2048)

        if data == b"FIN":
            print("Transmisión completa.")
            break

        try:
            partes = data.split(b"|", 1)
            seq = int(partes[0])
            fragmento = partes[1]
        except Exception as e:
            print("Paquete corrupto, ignorado:", e)
            continue

        if seq not in recibido:
            recibido[seq] = fragmento
            print(f"📥 Recibido paquete {seq}")
            porcentaje = (len(recibido) / 3200) * 100  # estimado
            print(f"Progreso: {porcentaje:.1f}%")

        ack = f"ACK|{seq}".encode()
        sock.sendto(ack, (SERVER_IP, SERVER_PORT))

    fin = time.time()
    print(f"⏱️ Tiempo total: {fin - inicio:.2f} segundos")

    # Reconstrucción
    with open("recibido.mp3", "wb") as f:
        for i in range(len(recibido)):
            f.write(recibido[i])

    print(" Archivo guardado como 'recibido.mp3'")

    try:
        print("🎶 Reproduciendo archivo...")
        playsound("recibido.mp3")
    except Exception:
        print("No se pudo reproducir automáticamente (verifica 'playsound')")

if __name__ == "__main__":
    cliente()



