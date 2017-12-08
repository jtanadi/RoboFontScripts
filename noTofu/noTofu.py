import string as s
import re
from vanilla import *

def removeExtraSpaces(inputString):
    return re.sub(r"\  +", " ", inputString)

class NoTofu(object):
    def __init__(self):
        self.inputText, self.tofuText = "", ""
        self.ucCheck, self.lcCheck, self.digitCheck, self.punctCheck = 0, 0, 0, 0

        self.window = Window((500, 610), "Mo Tofu Mo Problems")

        row = 10
        self.window.inputTitle = TextBox((10, row, 100, 20),
                                         "Input:")
        self.window.inputText = TextEditor((10, row+25, -10, 200),
                                           callback=self.inputTextCallback)

        row += 240
        self.window.tofuTitle = TextBox((10, row, 100, 20),
                                        "Tofu:")
        self.window.tofuText = EditText((10, row+25, -110, 50),
                                        callback=self.tofuTextCallback)

        self.window.ucCheck = CheckBox((400, row+8, 100, 20),
                                       "UC only",
                                       callback=self.ucCheckCallback)

        self.window.lcCheck = CheckBox((400, row+30, 100, 20),
                                       "lc only",
                                       callback=self.lcCheckCallback)

        self.window.digitCheck = CheckBox((400, row+52, 100, 20),
                                          "No digits",
                                          callback=self.digitCheckCallback)

        self.window.punctCheck = CheckBox((400, row+74, 100, 20),
                                          "No puncts.",
                                          callback=self.punctCheckCallback)

        row += 90
        self.window.tofuButton = Button((200, row, 100, 30),
                                        "No Mo Tofu!",
                                        callback=self.tofuButtonCallback)

        row += 25
        self.window.outputTitle = TextBox((10, row, 100, 20),
                                          "Output:")

        self.window.outputText = TextEditor((10, row+25, -10, 200),
                                            readOnly=True)

        self.window.open()

    def inputTextCallback(self, sender):
        self.inputText = sender.get()

    def tofuTextCallback(self, sender):
        self.tofuText = sender.get().replace(" ", "")

    def ucCheckCallback(self, sender):
        self.ucCheck = sender.get()
        self.window.lcCheck.set(0)
        self.lcCheck = 0

    def lcCheckCallback(self, sender):
        self.lcCheck = sender.get()
        self.window.ucCheck.set(0)
        self.ucCheck = 0

    def digitCheckCallback(self, sender):
        self.digitCheck = sender.get()

    def punctCheckCallback(self, sender):
        self.punctCheck = sender.get()

    def tofuButtonCallback(self, sender):
        outputText = self.inputText
        noBueno = self.tofuText

        if self.ucCheck == 1:
            outputText = self.inputText.upper()
            noBueno = noBueno.upper()

        if self.lcCheck == 1:
            outputText = self.inputText.lower()
            noBueno = noBueno.lower()

        if self.digitCheck == 1:
            noBueno += s.digits

        if self.punctCheck == 1:
            noBueno += s.punctuation + "‘’“”«»".decode("utf-8")

        # outputText = "".join(letter for letter in outputText if letter not in noBueno)
        # outputText = outputText.translate(None, noBueno)

        self.window.outputText.set(removeExtraSpaces(outputText))

NoTofu()

"""
---------------
     TO DO
---------------
+ Remove formatting from input (paste as plain text)
+ Add feature to add control chars
+ Better punctuation filter
"""
