"""
Servidor.

Este módulo implementa un servidor de logs que escucha mensajes entrantes en un puerto
específico y los guarda en un archivo .txt
"""
import socket
from datetime import datetime

#Configuración del host y puerto para el servidor de logs.
HOST = 'localhost' #Profe le saco la IP y el puerto para enviarlo.
PORT = 12345 #Profe le saco la IP y el puerto para enviarlo.

def iniciar_servidor():
    """
    Inicia el servidor de logs.

    El servidor escucha conexiones entrantes y, por cada mensaje recibido, añade un timestamp
    y lo guarda en el archivo 'log.txt'.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)  #Escucha una conexión a la vez
        print(f"Servidor de logs escuchando en el puerto {PORT}...")
        
        while True:
            conn, addr = s.accept()  #Acepta una nueva conexión
            with conn:
                print('Conectado por', addr)
                while True:
                    data = conn.recv(1024)  #Recibe datos del cliente
                    if not data:
                        break  #Si no hay datos, termina el bucle
                    
                    #Añade un timestamp al log
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"[{timestamp}] {data.decode('utf-8')}\n"
                    
                    #Guarda el log en un archivo
                    with open("log.txt", "a") as f:
                        f.write(log_entry)
                    
                    print(f"Log recibido: {log_entry.strip()}")
                    
if __name__ == "__main__":
    iniciar_servidor()