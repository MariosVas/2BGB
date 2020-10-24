from file_parser import load_json
import random

new_line = "\n"  # for f-strings

class WordsForMonsters:
    instructions = ""

    def __init__(self, guild, cards=None):
        self.game_guild = guild
        self.user_card_list_dict = {}
        if cards is None:
            self.cards = load_json()
        random.shuffle(self.cards)
        self.card_index = -1
        self.user_points = {}
        self.answer_list = []
        self.answer_to_user_list = []

    @classmethod
    def command_handler(cls, game, command, isDM, users=None, message_channel=None, user=None):
        if command == "":
            return "message channel", WordsForMonsters.instructions
        if "assign" in command or "give cards" in command or "top up" in command and not isDM:
            return "dm", game.give_cards(users)
        if "submit" in command:
            answers = command[8:].split(" ")
            return "message channel", game.handle_answers(answers, user)
        if "judge" in command:
            return "message channel", game.judge()
        if "choose" in command:
            chosen = int(command[8:])
            return "message channel", game.choose_answer(chosen)

    def give_cards(self, users):
        new_cards = {}
        for user in users:
            if not self.user_card_list_dict[user]:
                self.user_card_list_dict[user] = []
                self.user_points[user] = 0
            while len(self.user_card_list_dict[user]) < 10:
                card = self.get_card()
                self.user_card_list_dict[user].append(card)
                if new_cards[user]:
                    new_cards[user].append(card)
                else:
                    new_cards[user] = [card]
            if user not in self.user_points:
                self.user_points.append(user)
        return new_cards

    def get_card(self):
        self.card_index += 1
        return f"{self.card_index}__{self.cards[self.card_index]}"

    def handle_answers(self, answers, user):
        invalids = answers[:]
        indices_to_remove = []
        for index_of_word, user_word in self.user_card_list_dict[user]:
            for ans in answers:
                if user_word.startswith(ans):
                    invalids.pop(invalids.index(ans))
                    indices_to_remove.append(index_of_word)
        if len(invalids) < 1:
            for index_to_remove in indices_to_remove:
                self.answer_list.append(self.user_card_list_dict[user].pop(index_to_remove))
                self.answer_to_user_list.append(user)
            new_words = self.give_cards(user)
            return f"All good, answer accepted. New words: {new_line.join(new_words)}"
        else:
            return f"Answers with the following numbers were not accepted: {invalids}, please try again"

    def show_answers(self):
        not_submitted = []
        for user, user_words in self.user_card_list_dict.items():
            if len(user_words) >= 10:
                not_submitted.append(user)
        if len(not_submitted) > 0:
            return f"The following users have not submitted:{[f'{new_line}{user.name}' for user in not_submitted]}" \
                   f"\nPeople should not be afraid of their governments, and you should just submit an answer using " \
                   f"'!wfm submit X'"
        else:
            return "All have submitted! When ready type '!wfm show answers' to see them and '!wfm choose X'" \
                   " to choose an answer"

    def judge(self):
        check = self.show_answers()
        if check.startswith("All have submitted"):
            return [f"{new_line}{i}. {self.answer_list[i]}" for i in range(len(self.answer_list))]
        else:
            return check

    def choose_answer(self, choice):
        if self.show_answers().startswith("All have submitted"):
            return f"Congrats {self.answer_to_user_list[choice].name} you have gained a point.\n" \
                   f"Standings: {[' '.join((new_line ,  user , points)) for user, points in self.user_points.items()]}"
