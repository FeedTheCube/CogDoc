class Report(object):
    """description of class"""

    author = ""
    defaultOutput = "" #xls, csv, pdf
    lastModified = "" 

    queries = []
    dataItems = []
    
    #ADD - schedule
    #ADD - saved outputs

    def __init__(self, _xmlns, _useStyleVersion, _expressionLocale, _viewPagesAsTabs, element, name="unknown"):
        self.name = name
        self.xmlns = _xmlns
        self.useStyleVersion = _useStyleVersion
        self.expressionLocale = _expressionLocale
        self.viewPagesAsTabs = _viewPagesAsTabs
        self.element = element

    def json(self):
        return {
            'name': self.name,
            'xmlns' : self.xmlns, 
            'useStyleVersion' : self.useStyleVersion, 
            'expressionLocale' : self.expressionLocale, 
            'viewPagesAsTabs' : self.viewPagesAsTabs
        }

 