from file_parser import load_json
import random

new_line = "\n"  # for f-strings

class WordsForMonsters:
    instructions = ""

    def __init__(self, game_key, cards=None):
        self.game_key = game_key
        self.user_card_list_dict = {}
        if cards is None:
            self.questions, self.answers = load_json()
        random.shuffle(self.answers)
        random.shuffle(self.questions)
        self.card_index = -1
        self.user_points = {}
        self.answer_list = []
        self.answer_to_user_list = []
        self.current_question = None
        self.answer_delimiter = "[a]"

    @classmethod
    def command_handler(cls, game, command, is_dm, users=None, message_channel=None, user=None):
        if command == "":
            return "message channel", WordsForMonsters.instructions
        if "shuffle" in command:
            return "message channel", game.shuffle()
        if "assign" in command or "give cards" in command or "top up" in command and not is_dm:
            return "dm", game.give_cards(users)
        if "question" in command:
            return "message channel", message_channel, game.get_question()
        if "submit" in command:
            answers = command[8:].split(" ")
            return "dm", game.handle_answers(answers, user)
        if "judge" in command:
            return "message channel", message_channel, game.judge()
        if "choose" in command:
            chosen = int(command[8:])
            return "message channel", message_channel, game.choose_answer(chosen)
        if "show all" in command:
            return "dm", game.show_user_cards(user)

    def give_cards(self, users):
        new_cards = {}
        for user in users:
            if user not in self.user_card_list_dict:
                self.user_card_list_dict[user] = []
                self.user_points[user] = 0
            while len(self.user_card_list_dict[user]) < 10:
                card = self.get_card()
                self.user_card_list_dict[user].append(card)
                if user in new_cards:
                    new_cards[user] = f"{new_cards[user]}{new_line}{card}"
                else:
                    new_cards[user] = card
        return new_cards

    def show_user_cards(self, user):
        return {user: new_line.join(self.user_card_list_dict[user])}

    def get_card(self):
        self.card_index += 1
        return f"{self.card_index}. {self.answers[self.card_index]['text']}"

    def get_question(self):
        self.answer_list = []
        self.answer_to_user_list = []
        question = self.questions.pop()
        question["text"] = question["text"].replace("_", self.answer_delimiter)
        self.current_question = question
        return f"{question['text']}  / submit {question['numAnswers']} answer(s)."

    def shuffle(self):
        random.shuffle(self.questions)
        random.shuffle(self.answers)
        return "Why does my shuffling confuse you so? Decks re-shuffled"

    def handle_answers(self, answers, user):
        if self.current_question is None:
            return {user: "No active question, cannot submit answers"}
        invalids = answers[:]
        indices_to_remove = []
        for index_of_word, user_word in enumerate(self.user_card_list_dict[user]):
            for ans in answers:
                if user_word.startswith(ans):
                    invalids.pop(invalids.index(ans))
                    indices_to_remove.append(index_of_word)
        if len(invalids) < 1:
            list_of_answers = []
            pop_index_diff = 0
            for index_to_remove in indices_to_remove:
                list_of_answers.append(self.user_card_list_dict[user].pop(index_to_remove - pop_index_diff))
                pop_index_diff += 1
            self.answer_to_user_list.append(user)
            self.answer_list.append(list_of_answers)
            return {user: f"All good, answer accepted."}
        else:
            return {user: f"Answers with the following numbers were not accepted: {invalids}, please try again"}

    def show_answers(self):
        not_submitted = []
        for user, user_words in self.user_card_list_dict.items():
            if len(user_words) >= 10:
                not_submitted.append(user.name)
        if len(not_submitted) > 0:
            return f"The following users have not submitted: {new_line.join(not_submitted)}" \
                   f"\nPeople should not be afraid of their governments, and you should just submit an answer using " \
                   f"'!wfm submit X' in a private message to the bot"
        else:
            return "All have submitted! When ready type '!wfm show answers' to see them and '!wfm choose X'" \
                   " to choose an answer"

    def judge(self):
        check = self.show_answers()
        if self.current_question is None:
            return "No active question, command: '!wfm question'"
        if check.startswith("All have submitted"):
            temp_answer_list = []
            for index, answer_list in enumerate(self.answer_list):
                copy_of_question = f"{index}. {self.current_question['text']}"
                for answer in answer_list:
                    if self.answer_delimiter in copy_of_question:
                        copy_of_question = copy_of_question.replace(self.answer_delimiter,
                                                                    WordsForMonsters.clean_answer(answer), 1)
                    else:
                        copy_of_question = f"{copy_of_question} {WordsForMonsters.clean_answer(answer)}"
                temp_answer_list.append(copy_of_question)
            return new_line.join(temp_answer_list)
        else:
            return check
    @classmethod
    def clean_answer(cls, answer):
        return "".join(answer.split(".")[1:])

    def choose_answer(self, choice):
        if self.show_answers().startswith("All have submitted") and self.validate_choice(choice):
            self.current_question = None
            return f"Congrats {self.answer_to_user_list[choice].name} you have gained a point.\n" \
                   f"Standings: {[new_line.join((user.name , str(points))) for user, points in self.user_points.items()]}"
        else:
            return "Invalid choice or not all user have submitted"

    def validate_choice(self, choice):
        if self.answer_to_user_list[choice]:
            self.user_points[self.answer_to_user_list[choice]] += 1
            return True
        return False
