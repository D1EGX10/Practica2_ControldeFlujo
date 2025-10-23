import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5500  

def cliente():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        mensaje = "Hola servidor!"
        sock.sendto(mensaje.encode(), (SERVER_IP, SERVER_PORT))

        data, addr = sock.recvfrom(1024)
        print(f"Respuesta del servidor: {data.decode()}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    cliente()
