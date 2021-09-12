
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *
from googlesearch import search

import webbrowser
from urllib.error import *
import sys
import json
from tkinter.messagebox import *

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.initUI()
        self.show()
    
    def fetch(self):
        try:
            with open('previousText.json') as f:
                self.data = json.load(f)
        except:
            default_data = {"Query": "", "List": []}
            with open('previousText.json', 'w') as f:
                json.dump(default_data, f, indent=6)
            
            self.data = default_data

    def initUI(self):
        
        self.fetch()

        self.setWindowTitle("Plagiarism Detector")
        self.setWindowIcon(QtGui.QIcon("img.ico"))

        self.resize(300, 400)

        self.centralWidget = QWidget()

        self.layout = QGridLayout()

        self.qle = QTextEdit()
        self.qle.setText(self.data['Query'])

        self.submitButton = QPushButton("Look For Results")
        self.submitButton.clicked.connect(self.onClick)

        self.listObject = QListWidget()
        self.listObject.resize(120, 30)

        self.layout.addWidget(self.qle, 1, 2)
        self.layout.addWidget(self.listObject, 2, 2, 1, 3)
        self.layout.addWidget(self.submitButton, 3, 2)


        self.listObject.itemDoubleClicked.connect(self.onDoubleClick)

        en = enumerate(self.data['List'])
        for i, v in en:
            self.listObject.insertItem(i, v)

        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

    @pyqtSlot()
    def onClick(self):
        self.listObject.clear()
        query =  self.qle.toPlainText()

        if not query: return
        try:
            searchList = list(search(query, tld="co.in", num=10, stop=10, pause=2))
            for j in searchList:
                self.listObject.insertItem(self.listObject.count(), j)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error. You are offline.")
            msg.setWindowTitle('Error')
            msg.exec_()

    

    def onDoubleClick(self, a):
        webbrowser.open(a.text())

    def save(self):
        with open('previousText.json', 'w') as f:
            self.data['Query'] = self.qle.toPlainText()
            self.data['List'] = []

            print(self.data)
            if self.listObject.count() > 0:
                self.data['List'] = list(map(lambda a: str(a), [self.listObject.item(x).text() for x in range(self.listObject.count())]))
            
            json.dump(self.data, f, indent=6)

            


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Window()

    win.show()

    app.aboutToQuit.connect(win.save)

    sys.exit(app.exec_())
