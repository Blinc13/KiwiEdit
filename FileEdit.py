import tokenize

from io import StringIO
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QTimer

class FileEdit(QTextEdit):
    keywords: list
    timer: QTimer

    def __init__(self, keywords: list):
        super().__init__()

        self.keywords = keywords
        self.timer = QTimer(self)

        self.timer.start(400)
        self.timer.timeout.connect(self.update_syntax)

    def update_syntax(self):
        text = self.toPlainText()

        if len(text) == 0:
            return

        tokens = FileEdit.__generate_tokens_from_text(text)
        format_tokens_list = []

        for token in tokens:
            #if token.type == 0:  # If token.type is NAME
            token = Token(token.start, token.end, QBrush(QColor(255, 0, 0)))
            format_tokens_list.append(token)

        self.setPlainText("")

        lines = text.split('\n')

        for line_index in range(0, len(lines)):
            for char in range(0, len(lines[line_index])):
                brush = FileEdit.__get_brush_in_tokens(line_index, char, format_tokens_list)

                if brush is not None:
                    self.setTextColor(brush.color())

                    self.append(lines[line_index][char])
                else:
                    self.append(lines[line_index][char])


    def __get_brush_in_tokens(line: int, char: int, tokens: list):
        for token in tokens:
            if token.token_start <= (line, char) <= token.token_end:
                return token.brush

    def __generate_tokens_from_text(text: str):
        rd_line = StringIO(text)

        return tokenize.generate_tokens(rd_line.readline)


class Token:
    token_start: tuple
    token_end: tuple

    brush: QBrush

    def __init__(self, start, end, brush):
        self.token_start = start
        self.token_end = end

        self.brush = brush
