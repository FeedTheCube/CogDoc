class Report(object):
    """description of class"""

    author = ""
    defaultOutput = "" #xls, csv, pdf
    lastModified = "" 

    queries = []
    dataItems = []
    
    #ADD - schedule
    #ADD - saved outputs

    def __init__(self, _xmlns, _useStyleVersion, _expressionLocale, _viewPagesAsTabs):
        self.xmlns = _xmlns
        self.useStyleVersion = _useStyleVersion
        self.expressionLocale = _expressionLocale
        self.viewPagesAsTabs = _viewPagesAsTabs

    def json(self):
        return {
            'xmlns' : self.xmlns, 
            'useStyleVersion' : self.useStyleVersion, 
            'expressionLocale' : self.expressionLocale, 
            'viewPagesAsTabs' : self.viewPagesAsTabs
        }