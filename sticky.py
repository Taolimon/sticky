import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QGraphicsEffect, QGraphicsDropShadowEffect
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import random
import json


class StickyNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.stickyNotesArray = []
        self._SAVE_FILE = "sticky_notes.json"
        self.settings = Settings()
        self.loadNotes()

    def init_ui(self):
        self.setWindowTitle("Sticky Notes")
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet("background-color: #fffbcc;")  # sticky note yellow

        # create a button to add new notes
        self.button = QPushButton("new note")
        self.button.clicked.connect(self.showNewNote)

        # save notes
        self.saveButton = QPushButton("save notes")
        self.saveButton.clicked.connect(self.saveNotes)

        # load notes
        self.loadButton = QPushButton("load button")
        self.loadButton.clicked.connect(self.loadNotes)

        # create a text edit widget for the note
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet("font-size: 16px; border: none; background-color: #fffbcc;")
        self.text_edit.setText("Type your note here...")
        self.text_edit.setAlignment(Qt.AlignTop)

        # set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.loadButton)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def loadNotes(self):
        try:
            with open(self._SAVE_FILE, "r") as file:
                data = json.load(file)
                for note_data in data:
                    self.addNewNote(
                        note_data["id"],
                        note_data["text"],
                        note_data["x"],
                        note_data["y"]
                    )
        except FileNotFoundError:
            return []
        return
    
    def saveNotes(self):
        data = []
        for i in range(len(self.stickyNotesArray)):
            currentNote = self.stickyNotesArray[i]
            data.append({
                "id": currentNote.getNoteID(),
                "text": currentNote.text_edit.toPlainText(),
                "x": currentNote.pos().x(),
                "y": currentNote.pos().y(),
            })
        with open(self._SAVE_FILE, "w") as file:
            json.dump(data, file)
    
    def updateNotesArray():
        return
    
    def showNewNote(self, checked):
        newNote = StickyNote()
        self.stickyNotesArray.append(newNote)
        newNote.show()

    def addNewNote(self, id, text, x, y):
        newNote = StickyNote()
        newNote.loadNoteData(id, text, x, y)
        newNote.text_edit.setPalette(self.settings.colour_palette.currentGradient)
        self.stickyNotesArray.append(newNote)
        newNote.show()

class StickyNote(QWidget):
    # Appears as a free floating window if it has no parent
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_note()
        self.offset = None

    def init_note(self):
        self.noteID = random.randint(100000, 999999)
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet("background-color: #fffbcc; border-radius: 20px;")  # sticky note yellow
        self.setAttribute(Qt.WA_TranslucentBackground)

        # create a draggable header
        self.header = QWidget(self)
        self.header.setFixedHeight(20)
        self.header.setStyleSheet(
            "border: none; background-color: #fffbcc; border-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; padding: 5px;"
        )

        # create a text edit widget for the note
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet(
            "font-size: 16px; border: none; background-color: #fffbcc; border-radius: 5px; border-top-right-radius: 0px; border-top-left-radius: 0px; padding: 5px"
            )
        self.text_edit.setText("Type your note here...")
        self.text_edit.setAlignment(Qt.AlignTop)

        # Add effects
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(Qt.black)
        self.setGraphicsEffect(self.shadow)

        # set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.text_edit)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 20, 20, 20)
        container = QWidget()
        container.setLayout(layout)
        self.setLayout(layout)

    # Events
    
    def moveEvent(self, event):
        super(StickyNote, self).moveEvent(event)

    # On left mouse button press, set the sticky notes position to the mouse's
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    # When the mouse is moving and pressed, move to a new location based on the original 
    def mouseMoveEvent(self, event):
        if (self.offset != None and event.buttons() == Qt.LeftButton):
            self.move(self.pos() + event.pos() - self.offset)
        else:
            return super().mouseMoveEvent(event)

    # On mouse release, reset the offset back to none to integrate with the flow of
    # the other functions
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def getNoteID(self):
        return self.noteID
    
    def loadNoteData(self, id, text, x, y):
        self.id = id
        self.text_edit.setText(text)
        self.move(x, y)

class ColourPalette():
    def __init__(self):
        self.palettes = {
            'default' : {'background-color' : '#fffbcc' , 'text' : '#000000'},
            'dark' : {'background-color' : '#1f1f1f', 'text' : '#bbbbff'}
        }
        self.gradients = {
            'default' : self.getDefaultGradient(),
            'dark' : self.getDarkGradient(),
            'none' : None,
        }

        # Current variables
        self.currentPalette = self.palettes['default']
        self.currentGradient = self.gradients['default']
    
    def getDefaultGradient(self):
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(255, 251, 204))
        gradient.setColorAt(1.0, QColor(161, 128, 93))
        p.setBrush(QPalette.Window, QBrush(gradient))
        return p
    
    def getDarkGradient(self):
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(79, 79, 79))
        gradient.setColorAt(1.0, QColor(31, 31, 31))
        p.setBrush(QPalette.Window, QBrush(gradient))
        return p
        

class Settings():
    def __init__(self):
        self.colour_palette = ColourPalette()
        self.noteSize = (100, 100, 300, 300)
        self.Font = {
            'default' : {},
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StickyNoteApp()
    window.show()
    sys.exit(app.exec_())