"""The bot class"""
import random

class Bot:
    def __init__(self, input_session):
        self.session = input_session
        self.data_for_next_read = ""
        self.player_positions = {}

    def login(self):
        self.session.sendall(b"join|tronminator|GktQCxssIwvUBOoU\n")

    def new_game(self, player_id, map_width, map_height):
        print("New game started")
        self.player_id = player_id
        self.map_width = map_width
        self.map_height = map_height

    def play(self):
        session_as_file = self.session.makefile()

        while True:
            #print("Waiting for full data block...")
            byte_data = session_as_file.readline()
            #print("Received packet")
            self.parse_incoming_packet(str(byte_data))

    def make_next_move(self):
        direction = random.choice(["up", "down", "left", "right"])
        command = f"move|{direction}\n"
        self.session.sendall(bytes(command, 'utf-8'))
        print(f"Moved {direction}")

    def parse_incoming_packet(self, string_data):
        #print(string_data)
        string_data = string_data.split("\n")[0]
        splitted_string = string_data.split("|")
        #print(splitted_string)
        if "tick" in string_data:
            print(string_data)
            print(splitted_string)

        if splitted_string[0] == "lose":
            print("You lost the game")
        elif splitted_string[0] == "win":
            print("You won, congratulations!")
        elif splitted_string[0] == "message":
            pass
        elif splitted_string[0] == "die":
            pass
        elif splitted_string[0] == "tick":
            self.make_next_move()
        elif splitted_string[0] == "pos":
            pass
        elif splitted_string[0] == "error":
            pass
        elif splitted_string[0] == "motd":
            print("Received message of the day")
        elif splitted_string[0] == "game":
            self.new_game(splitted_string[1], splitted_string[2], splitted_string[3])
        elif splitted_string[0] == "error":
            print(f"Error received: {splitted_string[:-1]}")
