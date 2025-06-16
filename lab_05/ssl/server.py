import socket
import ssl
import threading

server_address = ('localhost', 12345)
clients = []

def handle_client(client_socket):
    clients.append(client_socket)
    print("Đã kết nối với:", client_socket.getpeername())
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
            # Gửi dữ liệu đến tất cả các client khác
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except:
                        try:
                            clients.remove(client)
                        except:
                            pass
    except:
        try:
            clients.remove(client_socket)
        except:
            pass
    finally:
        print("Đã ngắt kết nối:", client_socket.getpeername())
        try:
            clients.remove(client_socket)
        except:
            pass
        client_socket.close()

def main():
    # Tạo socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Server đang chờ kết nối...")

    # Tạo SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="./certificates/server-cert.crt",
                            keyfile="./certificates/server-key.key")

    while True:
        client_socket, client_address = server_socket.accept()

        # Thiết lập kết nối SSL
        ssl_socket = context.wrap_socket(client_socket, server_side=True)

        # Bắt đầu một luồng xử lý cho mỗi client
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
