from PyQt5.QtWidgets import QApplication
from FileEdit import FileEdit


app = QApplication([])

text_edit = FileEdit([])
text_edit.show()

app.exec()
