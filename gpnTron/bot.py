"""The bot class"""
import random

class Bot:
    def __init__(self, input_session):
        self.session = input_session
        self.data_for_next_read = ""
        self.player_positions = {}
        self.bot_player_id = 0
        self.current_bot_x = 0
        self.current_bot_y = 0
        self.map_x = 0
        self.map_y = 0
        self.last_map = []
        self.last_move_options = []
        self.last_direction = ""

    def login(self):
        self.session.sendall(b"join|tronminator|GktQCxssIwvUBOoU\n")

    def new_game(self, bot_player_id, map_width, map_height):
        print("New game started")
        self.bot_player_id = bot_player_id
        self.current_bot_x = 0
        self.current_bot_y = 0
        self.map_x = map_width
        self.map_y = map_height
        print(f"Map of this game: {self.map_x}x{self.map_y}")

    def play(self):
        session_as_file = self.session.makefile()

        while True:
            #print("Waiting for full data block...")
            byte_data = session_as_file.readline()
            #print("Received packet")
            self.parse_incoming_packet(str(byte_data))

    def get_map_obstacles(self):
        game_map = [['o'] * self.map_x for _ in range(self.map_y)]
        if len(self.player_positions) == 0:
            return game_map
    
        for positions in self.player_positions.values():
            for position in positions:
                game_map[position["x"]][position["y"]] = "!"
        
        game_map[self.current_bot_x][self.current_bot_y] = "@"
        return game_map

    def make_next_move(self):
        move_options = []

        game_map = self.get_map_obstacles()
        self.last_map = game_map

        left_x = (self.current_bot_x-1) % self.map_x
        right_x = (self.current_bot_x+1) % self.map_x
        top_y = (self.current_bot_y+1) % self.map_y
        down_y = (self.current_bot_y-1) % self.map_y

        if game_map[left_x][self.current_bot_y] == "o":
            move_options.append("left")
        if game_map[right_x][self.current_bot_y] == "o":
            move_options.append("right")
        if game_map[self.current_bot_x][top_y] == "o":
            move_options.append("up")
        if game_map[self.current_bot_x][down_y] == "o":
            move_options.append("down")

        self.last_move_options = move_options

        if len(move_options) == 0:
            move_options.append("up")
        direction = random.choice(move_options)
        self.last_direction = direction

        command = f"move|{direction}\n"
        self.session.sendall(bytes(command, 'utf-8'))
        print(f"Moved {direction}")

    def remove_player_from_map(self, player_id):
        print(f"Player {player_id} dies, deleting him from game")
        self.player_positions.pop(player_id, None)

    def add_player_position_to_map(self, player_id, x, y):
        try:
            self.player_positions[player_id].append({"x": x, "y": y})
        except KeyError:
            self.player_positions[player_id] = [{"x": x, "y": y}]
        # If its the own position, remember it
        if player_id == self.bot_player_id:
            self.current_bot_x = x
            self.current_bot_y = y

    def lose(self):
        print("Bot lost")
        print("Last map, options and direction:")
        print(self.last_map)
        print(self.last_move_options)
        print(self.last_direction)
        print("#################")

    def parse_incoming_packet(self, string_data):
        #print(string_data)
        string_data = string_data.split("\n")[0]
        splitted_string = string_data.split("|")
        #print(splitted_string)
        if "tick" in string_data:
            print(string_data)
            print(splitted_string)

        if splitted_string[0] == "game":
            self.new_game(int(splitted_string[3]), int(splitted_string[1]), int(splitted_string[2]))
        elif splitted_string[0] == "lose":
            self.lose()
        elif splitted_string[0] == "win":
            print("You won, congratulations!")
        elif splitted_string[0] == "tick":
            self.make_next_move()
        elif splitted_string[0] == "message":
            pass
        elif splitted_string[0] == "die":
            print("Player(s) died")
            self.remove_player_from_map(splitted_string[1])
        elif splitted_string[0] == "pos":
            print("Got player(s) position(s)")
            self.add_player_position_to_map(splitted_string[1], int(splitted_string[2]), int(splitted_string[3]))
        elif splitted_string[0] == "motd":
            print("Received message of the day")
        elif splitted_string[0] == "error":
            print(f"Error received: {splitted_string[:-1]}")
