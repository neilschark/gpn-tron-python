"""The bot class"""

class Bot:
    def __init__(self, input_session):
        self.session = input_session

    def login(self):
        self.session.sendall(b"join|tronminator|GktQCxssIwvUBOoU\n")

    def new_game(self, player_id, map_width, map_height):
        self.player_id = player_id
        self.map_width = map_width
        self.map_height = map_height

    def play(self):
        while True:
            print("Waiting for data")
            byte_data = self.session.recv(1024)
            self.parse_incoming_packet(byte_data)

    def parse_incoming_packet(self, byte_data):
        string_data = str(byte_data)
        #print(string_data)
        splitted_string = string_data.split("|")

        if splitted_string[0] == "lose":
            pass
        elif splitted_string[0] == "win":
            pass
        elif splitted_string[0] == "message":
            pass
        elif splitted_string[0] == "die":
            pass
        elif splitted_string[0] == "tick":
            pass
        elif splitted_string[0] == "pos":
            pass
        elif splitted_string[0] == "error":
            pass
        elif splitted_string[0] == "motd":
            pass
        elif splitted_string[0] == "game":
            self.new_game(splitted_string[1], splitted_string[2], splitted_string[3])
        elif splitted_string[0] == "error":
            pass
