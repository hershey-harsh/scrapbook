class Game:
    def __init__(self):
        self.current_room = None
        self.is_playing = True

    def start(self):
        print("Welcome to the Adventure Game!")
        self.is_playing = True
        self.create_rooms()
        self.current_room = self.rooms['start']

    def create_rooms(self):
        self.rooms = {
            'start': Room('Start Room', 'You are in a small room with a wooden door.'),
            'hallway': Room('Hallway', 'You are in a long hallway. There is a door at the end.'),
            'treasure': Room('Treasure Room', 'You found the treasure room! There is a chest here.')
        }
        self.rooms['start'].add_exit('north', self.rooms['hallway'])
        self.rooms['hallway'].add_exit('south', self.rooms['start'])
        self.rooms['hallway'].add_exit('north', self.rooms['treasure'])
        self.rooms['treasure'].add_exit('south', self.rooms['hallway'])

    def play(self):
        while self.is_playing:
            print(self.current_room.description)
            command = input("> ").strip().lower()
            self.process_command(command)

    def process_command(self, command):
        if command in ['quit', 'exit']:
            self.is_playing = False
            print("Thanks for playing!")
        elif command in self.current_room.exits:
            self.current_room = self.current_room.exits[command]
        else:
            print("You can't go that way.")

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}

    def add_exit(self, direction, room):
        self.exits[direction] = room

if __name__ == "__main__":
    game = Game()
    game.start()
    game.play()
