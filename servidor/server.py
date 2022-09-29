"""
    Servidor que recibe un registro desde al App principal
    lo muestra en consola y genera un archivo log

"""

import logging
import socketserver

global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        print("---" * 25)
        print(data.decode("UTF-32"))
        print("---" * 25)
        logging.basicConfig(filename="babuinos.log", level="DEBUG")
        logging.info(data.decode("UTF-32"))
        value2 = "Información recibida en el servidor"
        socket.sendto(value2.encode("UTF-32"), self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9000
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
