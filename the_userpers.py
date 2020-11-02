import random

new_line = "\n"  # for f-strings

class TheUserpers:
    instructions = ""

    def __init__(self, guild, channel):
        self.game_guild = guild
        self.game_channel = channel
    @classmethod
    def command_handler(cls, game, command, is_dm, users=None, message_channel=None, user=None):
        if command == "":
            return "message channel", TheUserpers.instructions
        if "shuffle" in command:
            return "message channel", game.shuffle()
        if "assign" in command and not is_dm:
            return "dm", game.give_cards(users)
        if "question" in command:
            return "message channel", message_channel, game.get_question()
        if "submit" in command:
            answers = command[8:].split(" ")
            return "message channel", message_channel, game.handle_answers(answers, user)
        if "judge" in command:
            return "message channel", message_channel, game.judge()
        if "choose" in command:
            chosen = int(command[8:])
            return "message channel", message_channel, game.choose_answer(chosen)

    def give_cards(self, users):
        new_cards = {}
        for user in users:
            if user.id not in self.user_card_list_dict:
                self.user_card_list_dict[user.id] = []
                self.user_points[user.id] = 0
            while len(self.user_card_list_dict[user.id]) < 10:
                card = self.get_card()
                self.user_card_list_dict[user.id].append(card)
                if user.id in new_cards:
                    new_cards[user.id] = f"{new_cards[user.id]}{new_line}{card}"
                else:
                    new_cards[user.id] = card
        return new_cards

    def get_card(self):
        self.card_index += 1
        return f"{self.card_index}. {self.answers[self.card_index]['text']}"

    def get_question(self):
        question = self.questions.pop()
        return f"{question['text']}  / submit {question['numAnswers']} answer(s)."

    def shuffle(self):
        random.shuffle(self.questions)
        random.shuffle(self.answers)
        return "Why does my shuffling confuse you so? Decks re-shuffled"

    def handle_answers(self, answers, user):
        invalids = answers[:]
        indices_to_remove = []
        print(self.user_card_list_dict)
        for index_of_word, user_word in enumerate(self.user_card_list_dict[user.id]):
            for ans in answers:
                if user_word.startswith(ans):
                    invalids.pop(invalids.index(ans))
                    indices_to_remove.append(index_of_word)
        if len(invalids) < 1:
            for index_to_remove in indices_to_remove:
                self.answer_list.append(self.user_card_list_dict[user.id].pop(index_to_remove))
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
