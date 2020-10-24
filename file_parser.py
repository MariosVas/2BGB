import json
import PyPDF2
import os


def parse_pdfs_for_words():
    words = []
    for file in os.listdir("."):
        if file.endswith(".pdf"):
            words.extend(parse_single_pdf_for_words(file))
    return words


def parse_single_pdf_for_words(filename):
    pdf_file = open(filename, "rb")
    reader = PyPDF2.PdfFileReader(pdf_file)
    words_as_list = []
    for i in range(1, 10):
        content = reader.getPage(i).extractText()
        string_temp = "".join(content.split("\n"))
        string_temp = "".join([j for j in string_temp if not j.isdigit()])
        words_as_list.extend(string_temp.split(". ")[1:])
    pdf_file.close()
    return words_as_list


def read_from_csv():
    words = []
    for file in os.listdir("."):
        if file.endswith(".csv"):
            with open(file, "r") as f:
                words.extend(f.read().split(", "))
    print(words)
    return words


def write_words_to_csv(filename, words):
    with open(f"{filename}.csv", "a") as f:
        [f.write(f"{word}, ") for word in words[:-2]]
        f.write(words[-1])


def load_json(filename="cards.json"):
    try:
        with open(filename, "r") as f:
            data = json.loads("".join(f.readlines()))
            answers = []
            questions = []
            for entry in data:
                if entry["cardType"] is "Q":
                    questions.append(entry)
                else:
                    answers.append(entry)
            return questions, answers
    except FileNotFoundError:
        print("File to load data from not found")
