import PyPDF2
import re

def parse_pdf_for_insider(pdf_name):
    pdf_file = open(pdf_name, "rb")
    reader = PyPDF2.PdfFileReader(pdf_file)
    print(reader.getNumPages(), " pages")
    words_as_list = []
    for i in range(1,10):
        content = reader.getPage(i).extractText()
        # print(content)
        string_temp = "".join(content.split("\n"))
        string_temp = "".join([j for j in string_temp if not j.isdigit()])
        words_as_list.extend(string_temp.split(". ")[1:])

    return words_as_list

