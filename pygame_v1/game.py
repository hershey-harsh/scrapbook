import pickle
import random

class Game:
    def __init__(self):
        self.current_room = None
        self.is_playing = True
        self.player = Player()
        self.enemies = {}
        self.quests = []

    def start(self):
        print("Welcome to the Adventure Game!")
        self.is_playing = True
        self.create_rooms()
        self.create_enemies()
        self.create_quests()
        self.current_room = self.rooms['start']

    def create_rooms(self):
        self.rooms = {
            'start': Room('Start Room', 'You are in a small room with a wooden door. There is a key here.'),
            'hallway': Room('Hallway', 'You are in a long hallway. There is a door at the end.'),
            'kitchen': Room('Kitchen', 'You are in a kitchen. There is a knife on the table.'),
            'library': Room('Library', 'You are in a library. There are many books on the shelves.'),
            'treasure': Room('Treasure Room', 'You found the treasure room! There is a chest here.'),
            'locked_room': Room('Locked Room', 'This room is locked. You need a key to enter.', locked=True, key_required='key'),
            'dark_room': Room('Dark Room', 'It is pitch black. You need a torch to see anything.', dark=True)
        }
        self.rooms['start'].add_exit('north', self.rooms['hallway'])
        self.rooms['hallway'].add_exit('south', self.rooms['start'])
        self.rooms['hallway'].add_exit('east', self.rooms['kitchen'])
        self.rooms['hallway'].add_exit('west', self.rooms['library'])
        self.rooms['hallway'].add_exit('north', self.rooms['treasure'])
        self.rooms['hallway'].add_exit('east', self.rooms['locked_room'])
        self.rooms['hallway'].add_exit('west', self.rooms['dark_room'])
        self.rooms['kitchen'].add_exit('west', self.rooms['hallway'])
        self.rooms['library'].add_exit('east', self.rooms['hallway'])
        self.rooms['treasure'].add_exit('south', self.rooms['hallway'])

        key = Item('key', 'A small rusty key.')
        chest = Item('chest', 'A large wooden chest. It seems to be locked.')
        knife = Item('knife', 'A sharp kitchen knife.')
        book = Item('book', 'A mysterious book with strange symbols.')
        potion = Item('potion', 'A healing potion that restores health.')
        torch = Item('torch', 'A torch to light up dark areas.')

        self.rooms['start'].add_item(key)
        self.rooms['treasure'].add_item(chest)
        self.rooms['kitchen'].add_item(knife)
        self.rooms['library'].add_item(book)
        self.rooms['kitchen'].add_item(potion)
        self.rooms['hallway'].add_item(torch)

    def create_enemies(self):
        goblin = Enemy('Goblin', 30, 5, [Item('gold', 'A small amount of gold.')])
        troll = Enemy('Troll', 50, 10, [Item('club', 'A heavy wooden club.')])
        self.enemies['library'] = goblin
        self.enemies['locked_room'] = troll

    def create_quests(self):
        quest1 = Quest('Find the Key', 'Find the key to unlock the locked room.', 'key', 'locked_room')
        quest2 = Quest('Defeat the Goblin', 'Defeat the goblin in the library.', 'Goblin', 'library', type='enemy')
        self.quests.append(quest1)
        self.quests.append(quest2)
        self.player.assign_quest(quest1)
        self.player.assign_quest(quest2)

    def play(self):
        while self.is_playing:
            print(self.current_room.description)
            if self.current_room.dark and not self.player.has_item('torch'):
                print("It is too dark to see anything. You need a torch.")
                command = input("> ").strip().lower()
                self.process_command(command)
                continue

            if self.current_room.locked:
                if self.player.has_item(self.current_room.key_required):
                    print("You use the key to unlock the room.")
                    self.current_room.locked = False
                else:
                    print("The room is locked. You need a key to enter.")
                    self.current_room = self.rooms['hallway']
                    continue

            if self.current_room.items:
                print("You see the following items:")
                for item in self.current_room.items:
                    print(f"- {item.name}")
            if self.current_room.name in self.enemies:
                enemy = self.enemies[self.current_room.name]
                print(f"You encounter a {enemy.name}!")
                combat = Combat(self.player, enemy)
                combat.start()
                if self.player.health <= 0:
                    print("You have been defeated!")
                    self.is_playing = False
                    return
                else:
                    loot = enemy.loot
                    for item in loot:
                        self.current_room.add_item(item)
                    del self.enemies[self.current_room.name]
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
        elif command == 'quests':
            self.player.show_quests()
        elif command.startswith('complete quest '):
            quest_name = command[len('complete quest '):]
            self.complete_quest(quest_name)
        elif command.startswith('combine '):
            items = command.split(' ')[1:]
            self.combine_items(items)
        elif command == 'save':
            self.save_game()
        elif command == 'load':
            self.load_game()
        elif command == 'map':
            self.show_map()
        else:
            print("I don't understand that command.")

    def use_item(self, item_name):
        item = self.player.get_item(item_name)
        if item:
            if item.name == 'key' and self.current_room.name == 'Treasure Room':
                print("You use the key to open the chest. You found the treasure! You win!")
                self.is_playing = False
            elif item.name == 'potion':
                self.player.health = min(self.player.max_health, self.player.health + 20)
                self.player.remove_item(item)
                print("You used a potion and restored your health.")
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

    def complete_quest(self, quest_name):
        for quest in self.player.quests:
            if quest.name == quest_name and quest.target_item in [i.name for i in self.player.inventory]:
                if self.current_room.name == quest.target_room:
                    print(f"You have completed the quest: {quest.name}")
                    self.player.quests.remove(quest)
                else:
                    print("You are not in the correct room to complete this quest.")
                return
        print(f"You haven't completed the quest: {quest_name}")

    def combine_items(self, items):
        item_objects = [self.player.get_item(item) for item in items]
        if all(item_objects):
            new_item = Item(' '.join(items), 'A combined item.')
            for item in item_objects:
                self.player.remove_item(item)
            self.player.add_item(new_item)
            print(f"You combined {', '.join(items)} into a new item: {new_item.name}")
        else:
            print("You don't have all the items to combine.")

    def save_game(self):
        with open('savegame.pkl', 'wb') as f:
            pickle.dump(self, f)
        print("Game saved successfully.")

    def load_game(self):
        global game
        with open('savegame.pkl', 'rb') as f:
            game = pickle.load(f)
        print("Game loaded successfully.")

    def show_map(self):
        print("Map of the game:")
        for room_name, room in self.rooms.items():
            print(f"{room_name}: {room.description}")

class Player:
    def __init__(self):
        self.inventory = []
        self.health = 100
        self.max_health = 100
        self.attack_power = 10
        self.quests = []
        self.inventory_limit = 5

    def add_item(self, item):
        if len(self.inventory) < self.inventory_limit:
            self.inventory.append(item)
        else:
            print("Your inventory is full. You can't carry any more items.")

    def get_item(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        return None

    def has_item(self, name):
        for item in self.inventory:
            if item.name == name:
                return True
        return False

    def remove_item(self, item):
        self.inventory.remove(item)

    def show_inventory(self):
        if self.inventory:
            print("You have the following items:")
            for item in self.inventory:
                print(f"- {item.name}: {item.description}")
        else:
            print("You have no items.")

    def assign_quest(self, quest):
        self.quests.append(quest)
        print(f"New quest assigned: {quest.name}")

    def show_quests(self):
        if self.quests:
            print("You have the following quests:")
            for quest in self.quests:
                print(f"- {quest.name}: {quest.description}")
        else:
            print("You have no quests.")

class Room:
    def __init__(self, name, description, locked=False, key_required=None, dark=False):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.locked = locked
        self.key_required = key_required
        self.dark = dark

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

class Enemy:
    def __init__(self, name, health, attack_power, loot):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.loot = loot

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start(self):
        while self.player.health > 0 and self.enemy.health > 0:
            print(f"Player Health: {self.player.health}, {self.enemy.name} Health: {self.enemy.health}")
            action = input("Do you want to 'attack' or 'run'? ").strip().lower()
            if action == 'attack':
                self.enemy.health -= self.player.attack_power
                print(f"You attack the {self.enemy.name}!")
                if self.enemy.health <= 0:
                    print(f"You defeated the {self.enemy.name}!")
                    return
                self.player.health -= self.enemy.attack_power
                print(f"The {self.enemy.name} attacks you!")
            elif action == 'run':
                print("You run away!")
                return
            else:
                print("Invalid action.")
        if self.player.health <= 0:
            print("You have been defeated!")

class Quest:
    def __init__(self, name, description, target_item, target_room, type='item'):
        self.name = name
        self.description = description
        self.target_item = target_item
        self.target_room = target_room
        self.type = type

if __name__ == "__main__":
    game = Game()
    game.start()
    game.play()
