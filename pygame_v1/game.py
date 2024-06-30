class Game:
    def __init__(self):
        self.current_room = None
        self.is_playing = True
        self.player = Player()

    def start(self):
        print("Welcome to the Adventure Game!")
        self.is_playing = True
        self.create_rooms()
        self.current_room = self.rooms['start']

    def create_rooms(self):
        self.rooms = {
            'start': Room('Start Room', 'You are in a small room with a wooden door. There is a key here.'),
            'hallway': Room('Hallway', 'You are in a long hallway. There is a door at the end.'),
            'kitchen': Room('Kitchen', 'You are in a kitchen. There is a knife on the table.'),
            'library': Room('Library', 'You are in a library. There are many books on the shelves.'),
            'treasure': Room('Treasure Room', 'You found the treasure room! There is a chest here.')
        }
        self.rooms['start'].add_exit('north', self.rooms['hallway'])
        self.rooms['hallway'].add_exit('south', self.rooms['start'])
        self.rooms['hallway'].add_exit('east', self.rooms['kitchen'])
        self.rooms['hallway'].add_exit('west', self.rooms['library'])
        self.rooms['hallway'].add_exit('north', self.rooms['treasure'])
        self.rooms['kitchen'].add_exit('west', self.rooms['hallway'])
        self.rooms['library'].add_exit('east', self.rooms['hallway'])
        self.rooms['treasure'].add_exit('south', self.rooms['hallway'])

        key = Item('key', 'A small rusty key.')
        chest = Item('chest', 'A large wooden chest. It seems to be locked.')
        knife = Item('knife', 'A sharp kitchen knife.')
        book = Item('book', 'A mysterious book with strange symbols.')

        self.rooms['start'].add_item(key)
        self.rooms['treasure'].add_item(chest)
        self.rooms['kitchen'].add_item(knife)
        self.rooms['library'].add_item(book)

    def play(self):
        while self.is_playing:
            print(self.current_room.description)
            if self.current_room.items:
                print("You see the following items:")
                for item in self.current_room.items:
                    print(f"- {item.name}")
            command = input("> ").strip().lower()
            self.process_command(command)

    def process_command(self, command):
        if command in ['quit', 'exit']:
            self.is_playing = False
            print("Thanks for playing!")
        elif command.startswith('go '):
            direction = command.split(' ')[1]
            if direction in self.current_room.exits:
                self.current_room = self.current_room.exits[direction]
            else:
                print("You can't go that way.")
        elif command.startswith('take '):
            item_name = command.split(' ')[1]
            item = self.current_room.get_item(item_name)
            if item:
                self.player.add_item(item)
                self.current_room.remove_item(item)
                print(f"You picked up the {item.name}.")
            else:
                print("There's no such item here.")
        elif command == 'inventory':
            self.player.show_inventory()
        elif command.startswith('use '):
            item_name = command.split(' ')[1]
            self.use_item(item_name)
        elif command.startswith('inspect '):
            item_name = command.split(' ')[1]
            self.inspect_item(item_name)
        else:
            print("I don't understand that command.")

    def use_item(self, item_name):
        item = self.player.get_item(item_name)
        if item:
            if item.name == 'key' and self.current_room.name == 'Treasure Room':
                print("You use the key to open the chest. You found the treasure! You win!")
                self.is_playing = False
            else:
                print(f"You can't use the {item.name} here.")
        else:
            print(f"You don't have a {item_name}.")

    def inspect_item(self, item_name):
        item = self.player.get_item(item_name)
        if item:
            print(f"Inspecting {item.name}: {item.description}")
        else:
            print(f"You don't have a {item_name}.")

class Player:
    def __init__(self):
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def get_item(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        return None

    def show_inventory(self):
        if self.inventory:
            print("You have the following items:")
            for item in self.inventory:
                print(f"- {item.name}: {item.description}")
        else:
            print("You have no items.")

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

if __name__ == "__main__":
    game = Game()
    game.start()
    game.play()
