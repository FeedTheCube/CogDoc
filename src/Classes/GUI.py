import tkinter
import os
from src.Classes.Util import Util
from src.Classes.Query import Query
from tkinter import filedialog

class GUI(object):
    """description of class"""

    reports = []

    def setInputFile(self):
        inputFile = filedialog.askopenfilename(initialdir = "./",title = "Choose an input file",filetypes = (("XML Files","*.xml"),("All Files","*.*")))
        if inputFile:
            self.inputName['text'] = inputFile
            self.content, self.report = Util.loadInputFile(inputFile)
        else:
            self.inputName['text'] = "No Input File Selected"

    def setOutputFile(self):
        outputFile =  filedialog.asksaveasfilename(initialdir = "./Output/",title = "Choose an output file",filetypes = (("HTML Files","*.html"),("CSV Files","*.csv"),("All Files","*.*")))
        if outputFile:
            self.outputName['text'] = outputFile
        else:
            self.outputName['text'] = "No Output File Selected"


    def doExport(self):

        #CHANGE - This needs to handle outputting multiple reports to a single file
        #ADD - should also make sure the correct extension is on the filename

        if(os.path.exists(self.inputName['text']) and os.path.isfile(self.inputName['text']) and self.outputName['text'] != ""):
            if self.content:
                Util.exportHTML(self.outputName['text'], self.report.name, self.report.name, self.content, "FOOTER")


    def draw(self):
        root = tkinter.Tk()

        frame = tkinter.Frame(root)
        frame.pack()

        self.inputName = tkinter.Label(frame, text="No Input File Selected", anchor="w", width=40)
        self.outputName = tkinter.Label(frame, text="No Output File Selected", anchor="w", width=40)

        self.inputName.pack(side=tkinter.LEFT)

        buttonIn = tkinter.Button(frame, 
                           text="Choose",
                           command=self.setInputFile)
        buttonIn.pack(side=tkinter.LEFT)


        self.outputName.pack(side=tkinter.LEFT)

        buttonOut = tkinter.Button(frame,
                           text="Choose",
                           command=self.setOutputFile)
        buttonOut.pack(side=tkinter.LEFT)


        buttonExport = tkinter.Button(frame,
                           text="Export",
                           command=self.doExport)
        buttonExport.pack(side=tkinter.LEFT)

        root.mainloop()