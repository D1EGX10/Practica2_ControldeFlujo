import socket

SERVER_IP = "127.0.0.1"  
SERVER_PORT = 5500      

def servidor():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((SERVER_IP, SERVER_PORT))
        print(f"Servidor UDP escuchando en {SERVER_IP}:{SERVER_PORT}")

        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Mensaje recibido de {addr}: {data.decode()}")
            sock.sendto(b"ACK", addr)

    except PermissionError:
        print(f"No se pudo abrir el puerto {SERVER_PORT}. Prueba otro puerto o ejecuta como administrador.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    servidor()
