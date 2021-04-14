import socket
serversocket = socket.socket()
serversocket.bind(("127.0.0.1", 8080))
serversocket.listen(8080)

def process_input(recvdata):
    msg = open("index.html", "rb").read()
    msg = "HTTP/1.0 200 OK\r\nServer: ls\r\nContent-Type: text/html\r\n\r\n".encode('UTF-8') + msg
    return msg
while True:
    (clientsocket, address) = serversocket.accept()
    receive_data = ''.encode('UTF-8')
    while True:
        receive_data += clientsocket.recv(4096)
        if "\r\n\r\n".encode('UTF-8') in receive_data:
            response_msg = process_input(receive_data)
    clientsocket.send(response_msg)
    clientsocket.close()