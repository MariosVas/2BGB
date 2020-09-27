import pdf_parse

class InsiderGame:
    words = []

    def __init__(self, words=pdf_parse.parse_pdf_for_insider("CustomInsider_PnP.pdf")):
        self.words = words

