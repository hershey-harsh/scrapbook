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
            'locked_room': Room('Locked Room', 'This room is locked. You need a key to enter.', locked=True)
        }
        self.rooms['start'].add_exit('north', self.rooms['hallway'])
        self.rooms['hallway'].add_exit('south', self.rooms['start'])
        self.rooms['hallway'].add_exit('east', self.rooms['kitchen'])
        self.rooms['hallway'].add_exit('west', self.rooms['library'])
        self.rooms['hallway'].add_exit('north', self.rooms['treasure'])
        self.rooms['hallway'].add_exit('east', self.rooms['locked_room'])
        self.rooms['kitchen'].add_exit('west', self.rooms['hallway'])
        self.rooms['library'].add_exit('east', self.rooms['hallway'])
        self.rooms['treasure'].add_exit('south', self.rooms['hallway'])

        key = Item('key', 'A small rusty key.')
        chest = Item('chest', 'A large wooden chest. It seems to be locked.')
        knife = Item('knife', 'A sharp kitchen knife.')
        book = Item('book', 'A mysterious book with strange symbols.')
        potion = Item('potion', 'A healing potion that restores health.')

        self.rooms['start'].add_item(key)
        self.rooms['treasure'].add_item(chest)
        self.rooms['kitchen'].add_item(knife)
        self.rooms['library'].add_item(book)
        self.rooms['kitchen'].add_item(potion)

    def create_enemies(self):
        goblin = Enemy('Goblin', 30, 5)
        troll = Enemy('Troll', 50, 10)
        self.enemies['library'] = goblin
        self.enemies['locked_room'] = troll

    def create_quests(self):
        quest = Quest('Find the Key', 'Find the key to unlock the locked room.', 'key', 'locked_room')
        self.quests.append(quest)
        self.player.assign_quest(quest)

    def play(self):
        while self.is_playing:
            print(self.current_room.description)
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
        elif command.startswith('quests'):
            self.player.show_quests()
        elif command.startswith('complete quest '):
            quest_name = command[len('complete quest '):]
            self.complete_quest(quest_name)
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
            if quest.name == quest_name and quest.target_item in self.player.inventory:
                if self.current_room.name == quest.target_room:
                    print(f"You have completed the quest: {quest.name}")
                    self.player.quests.remove(quest)
                else:
                    print("You are not in the correct room to complete this quest.")
                return
        print(f"You haven't completed the quest: {quest_name}")

class Player:
    def __init__(self):
        self.inventory = []
        self.health = 100
        self.max_health = 100
        self.attack_power = 10
        self.quests = []

    def add_item(self, item):
        self.inventory.append(item)

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

# This is what I was able to do this hour. I was told it's fine to submit "incomplete" code and to submit whatever I have by the end of the hour.