import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def inform_user(parent, text):
    ans = QMessageBox.information(
        parent, None, text,
        QMessageBox.Ok | QMessageBox.Cancel
    )
    return ans

class Tutorial(object):

    def __int__(self):
        super(Tutorial, self).__init__()

        # self.start_tutorial()

    def start_tutorial(self, parent):
        text = "Welcome to BZMAN tutorial!\nThis will be a short guide to show you the features of BZMAN.\n\n"
        text +="Let's start by creating a new file. Click 'Ok' to continue."
        ans = inform_user(parent, text)
        return ans

        # if ans == QMessageBox.Ok:
        #     print("yes begin tutorial")
    
    def new_entry(self, parent):
        text = "Enter"
        inform_user(parent, text)