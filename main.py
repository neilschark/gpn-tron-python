import socket
from gpnTron.bot import Bot

HOST = "localhost" #"gpn-tron.duckdns.org"  # The server's hostname or IP address
PORT = 4000  # The port used by the server


def main():
    print("Bot started")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        bot = Bot(s)
        bot.login()
        bot.play()

if __name__ == "__main__":
    main()
    