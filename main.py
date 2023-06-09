import socket

HOST = "gpn-tron.duckdns.org"  # The server's hostname or IP address
PORT = 4000  # The port used by the server


def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"join|tronminator|GktQCxssIwvUBOoU\n")
        while True:
            print("Waiting for data")
            data = s.recv(1024)
            print(data)

def main():
    print("Bot started")
    receive_data()



if __name__ == "__main__":
    main()
    