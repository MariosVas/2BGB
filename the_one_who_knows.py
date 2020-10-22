import random
import time
from datetime import datetime


class TheOneWhoKnows:
    commands_for_game = "'!towk assign' will assign roles to players," \
                       "'!towk start' will start the timer (this is when you start asking the master)" \
                       "To see the remaining time either '!towk timer left' or '!time' (although with multiple games this might bug)"
    instructions = "Game Master: You know the word, you want the players to find the word, you can answer questions with Yes, No or Maybe.\n" \
                   "Plebs: Self explanatory really, you ask questions to find the word.\n" \
                   "The One Who Knows (OWK): You know the word, you have to help the Plebs find the word without them realising you are The One Who Knows (by also asking questions\n" \
                   "After the timer runs out, the Game Master will receive a direct message saying so. If they players haven't found the word they've lost." \
                   "If the players find the word before the time runs out, they have one chance to vote who the OWK is. " \
                   "They find the OWK they win, they don't find the  OWK they lose.\n" \
                   "Commands: '!towk assign' to assign roles (every played in a voice channel gets a "
    default_words = ['Apple', 'Boat', 'Toaster', 'Skyscraper', 'Car', 'Airplane', 'CD', 'Roof', 'Table', 'Pen', 'Computer', 'Lamp', 'Shorts', 'Jack-o-Lantern', 'Easter', 'January', 'Horse', 'Prisoner', 'Truck', 'King', 'Game', 'Pool', 'Software', 'Television', 'Garage', 'Drugstore', 'Highway', 'Toll Booth', 'Tire', 'Spoon', 'Wood', 'Fire', 'Soil', 'Gold', 'Water', 'Air', 'Calendar', 'Vase', 'Bucket', 'Basket', 'Bowl', 'Trash Can', 'Cane', 'Straw', 'Tube', 'Telescope', 'Cane', 'Umbrella', 'Jupiter', 'Rome', 'Spain', 'Japan', 'The Moon', 'Peanut Butter', 'Battery', 'Unicycle', 'Toilet', 'Tree', 'Couch', 'Picture', 'Farm', 'Cardboard', 'Camera', 'Movie', 'Window', 'Kitten', 'Reindeer', 'Drum', 'Bird', 'Coast', 'Glass', 'Meteor', 'Indian', 'Magic', 'Red', 'Intersection', 'Review', 'Geek', 'Bear', 'Printer', 'Guitar', 'Cracker', 'Microphone', 'Door', 'Pillow', 'Square', 'Keyboard', 'Mouse', 'Eye', 'Stocking',
             'Scissors', 'Cup', 'Envelope', 'Celebrity', 'Cat', 'Dog', 'Guinea Pig', 'Pumpkin', 'Pants', 'Artist', 'Imposter', 'YouTube', 'Fork', 'Driveway', 'Flag', 'Book', 'Cloud', 'Elf', 'China', 'Christmas', 'Holiday', 'Snow', 'Penguin', 'Polar Bear', 'Dad', 'Pencil', 'Trumpet', 'Ukelele', 'Box', 'Palm Tree', 'Store', 'Game', 'Advertisement', 'Taco', 'Ribs', 'Macaroni & Cheese', 'Galaxy', 'Traitor', 'Laptop', 'History', 'Xbox', 'Playstation', 'Smile', 'Fish', 'Brick', 'Lego', 'Watch', 'Clock', 'Block', 'Friend', 'Pot', 'Squat', 'Hat', 'WiÞ', 'Network', 'Tattoo', 'Desert', 'Kangaroo', 'Purse', 'Beach', 'Exercise', 'Frog', 'Spring', 'England', 'Paws', 'Comedian', 'Tennessee', 'Beyonce', 'Email', 'Hello Kitty', 'Fox', 'Dolphin', 'Present', 'Portrait', 'Blade', 'Whip', 'Foot', 'Robot', 'Cake', 'Pudding', 'Ice', 'Milk', 'Cheese', 'Prayer', 'Mask', 'Gun', 'Dynamite', 'France', 'Crayon', 'Shirt',
             'Beard', 'Fantasy', 'Wrong', 'Right', 'Netlix', 'Finger', 'Toothpaste', 'Teddy Bear', 'Fashion', 'Sign', 'Facebook', 'Twitter', 'Block', 'Desk', 'Chair', 'Key', 'Lock', 'Sidewalk', 'Starbucks', 'Astronaut', 'Ghost', 'Wind', 'Sandwich', 'Pie', 'Hair', 'Makeup', 'Bathtub', 'Shower', 'Wings', 'Water', 'Potato', 'Elbow', 'Sweatpants', 'Hamburger', 'Snack', 'Pepsi', 'Eyelash', 'Basketball', 'Baseball', 'Scoreboard', 'Hot Dog', 'Slave', 'Mermaid', 'Tiger', 'Bow Tie', 'Suit', 'Piano', 'Bikini', 'Tear', 'Swim', 'Phone', 'Ashtray', 'Gold', 'Airport', 'Time', 'Prince', 'Bunny', 'Bed', 'High School', 'Stairwell', 'Unicorn', 'Tomato', 'Spaceship', 'DVD', 'Sword', 'Tent', 'Machine', 'Frying Pan', 'Sink', 'Towel', 'Vacation', 'Rocket', 'Fireworks', 'Space', 'Alien', 'Washer', 'Trunk', 'Hammock', 'Fountain', 'Boat', 'Light', 'Alley', 'Beer', 'Vitamin', 'Adult', 'Infant', 'Diaper', 'Brother', 'Sister',
             'Launchpad', 'Sock', 'Veterinarian ', 'Library', 'Sunglasses', 'Blue', 'Slippers', 'Jewel', 'Halloween', 'Bride', 'Mountain', 'River', 'Canyon', 'Pony', 'Storm', 'Asteroid', 'Wolf', 'Dirt', 'Boy', 'Doll', 'Termite', 'Cigarette', 'Jar', 'Hole', 'Skateboard', 'Banana', 'Crown', 'Circuit', 'Lightning', 'Garbage', 'Gasoline', 'Flower', 'Grass', 'OfÞce', 'Script', 'Explosion', 'Contract', 'Sock', 'Lettuce', 'Pin', 'Needle', 'Dump Truck', 'Construction', 'Human', 'Shrub', 'Toast', 'Smartphone', 'Money', 'Hug', 'Actress', 'Award', 'Sneaker', 'Tuxedo', 'Cherry', 'Peanut', 'Secret', 'Drawing', 'Castle', 'Jaguar', 'Jacket', 'Puppy', 'Bus', 'Cow', 'President', 'Ribbon', 'Conversation', 'Ankle', 'Romance', 'Music', 'Challenge', 'Prize', 'Fun', 'New', 'Dream', 'Love', 'Party', 'Voice', 'Fire', 'Thief', 'Bed', 'Junk', 'God', 'Nightmare', 'Laugh', 'Hammer', 'Park', 'London', 'Heart', 'Night', 'Minute',
             'Sentence', 'Elevator', 'Jellybean', 'Ocean', 'Point', 'Answer', 'Shovel', 'Grin', 'Hour', 'Body', 'Floor', 'Class', 'Surprise', 'Microwave', 'Waterfall', 'Elephant', 'Radio', 'Magnet', 'Barber', 'Desert', 'Idea', 'Shirt', 'Pizza', 'Bowling', 'Brain', 'Brochure', 'Close', 'Sugar', 'Swamp', 'Rat', 'Loud', 'Gear', 'Purple', 'Brown', 'Artwork', 'Money', 'River', 'Pepper', 'Pig', 'Corporation', 'Sneeze', 'Egg', 'Escape', 'Santa Claus', 'Path', 'Exercise', 'Fear', 'Rules', 'Three', 'Army', 'Cattle', 'Ant', 'Fleet', 'Bees', 'Pride', 'Bandage', 'Igloo', 'Lips', 'Paint', 'Cartoon', 'Photograph', 'Hill', 'Nest', 'Director', 'Credit Card', 'Toenail', 'Shoulder', 'Outside', 'Sweet', 'Square', 'Plain', 'Measure', 'Mind', 'Chocolate', 'Pajamas', 'Train', 'Children', 'Planet', 'Bookcase', 'Engine', 'Sand', 'Nurse', 'Dancer', 'Curtain', 'Bottle', 'Monkey', 'Daisy', 'Tablecloth', 'Cupcake', 'Leg', 'Continent',
             'Room', 'Lipstick', 'Star', 'Chicken', 'Court', 'Family', 'Peanut', 'Banana', 'CatÞsh', 'Checkmate', 'Chopstick', 'Workshop', 'Country', 'Website', 'State', 'Iceberg', 'Teaspoon', 'Password', 'Teeth', 'Drill', 'Apple', 'Professor', 'Bell', 'Octopus', 'Football', 'Calendar', 'Lady', 'Lion', 'Rabbit', 'Pinwheel', 'Skin', 'Tractor', 'Slime', 'Kidney', 'Magazine']
    words = []
    timer_length = 180
    master = None
    timer = None
    game_guild = None

    def __init__(self, guild, words=None):
        game_guild = guild
        if words is None:
            words = TheOneWhoKnows.default_words
        self.words = words
        self.timeLeft = time

    # command should be the string after !twok
    @classmethod
    async def command_handler(cls, game, command, users=None, timer=None):
        if command == "":
            return "message channel", TheOneWhoKnows.commands_for_game, TheOneWhoKnows.instructions
        if "assign" in command:
            print(len(users))
            roles = game.assign_roles(users)
            while len(users) < 3:
            # while roles == "not enough players":
                # return "message channel", 'Not enough players to assign roles'
                users.append(users[0])
            print(len(users))
            user_to_dm_dict = {}
            for i in range(len(users)):
                user_to_dm_dict[users[i].id] = roles[i]
            return "dm", user_to_dm_dict
        if command.startswith("set timer"):
            game.timer_length = int(command[10:])
            return "none"
        if "start" in command:
            game.timer = timer
            game.start_timer(timer)
            return "timer started", game.timer_length
        if "timer left" in command:
            return "timer left", game.timer_left()

    def assign_roles(self, user_list):
        while len(user_list) < 3:
            # return "not enough players"
            user_list.append(user_list[0])
        word = self.get_random_word()
        roles = [f"Game Master - word: {word}", f"The One Who Knows - word: {word}"]
        [roles.append("Pleb") for i in range(len(user_list)-2)]
        if len(roles) >= 10:
            roles[-1] = f"The One Who Knows - word: {word}"
        random.shuffle(roles)
        self.master = user_list[roles.index(f"Game Master - word: {word}")]
        return roles

    def get_random_word(self):
        return random.choice(self.words)

    def start_timer(self, timer):
        self.timer = timer
        self.timer.start()

    def timer_left(self):
        time_to_give = self.timer_length - (time.time() - self.timer.started_at)
        return time_to_give if time_to_give > 0 else 0
