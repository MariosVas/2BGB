class PoliticalRevolution:
    instructions = ""

    def __init__(self, guild):
        self.game_guild = guild

    def command_handler(cls, game, command, users=None, timer=None):
        if command == "":
            return "message channel", PoliticalRevolution.instructions
        if "assign" in command:
            return