class Style(object):
    """description of class"""

    #Seemed like this should be a class so it can keep track of the whole "tree" of styles, 
    #with each building on the one above it

    reference = ""
    css = []
    parent = None

    def __init__(self, parent = None, reference = "", css = ""):
        self.parent = parent
        self.reference = reference
        self.css.append(css)

    def getStyleTree(self):
        allStyles = []
        if self.css != "":
           allStyles.append(self.css)

        if self.reference != "":
            allStyles.append(self.reference)

        if(self.parent != None):
            allStyles.append(self.parent.getStyleTree())

        #NOTE - styles should be returned so that [0] is the one that over-rules everything after

        return allStyles

    def debug(self):
        print(self.getStyleTree())