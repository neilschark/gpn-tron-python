import socket

HOST = "gpn-tron.duckdns.org"  # The server's hostname or IP address
PORT = 4000  # The port used by the server

def login(s):
    s.sendall(b"join|tronminator|GktQCxssIwvUBOoU\n")

def parse_incoming_packet(byte_data):
    string_data = str(byte_data)
    print(string_data)

def receive_data(s):
    while True:
        print("Waiting for data")
        byte_data = s.recv(1024)
        parse_incoming_packet(byte_data)


def main():
    print("Bot started")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        login(s)
        receive_data(s)

if __name__ == "__main__":
    main()
    