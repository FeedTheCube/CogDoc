class Report(object):
    """description of class"""

    author = ""
    defaultOutput = "" #xls, csv, pdf
    lastModified = "" 

    queries = []
    dataItems = []
    
    #ADD - schedule
    #ADD - saved outputs

    def __init__(self, CMID, name, xmlns, useStyleVersion, expressionLocale,  element, viewPagesAsTabs=None, drillBehaviors = [], queries=[], dataItems=[], pages=[], dataContainers=[]):
        self.CMID = CMID
        self.xmlns = xmlns
        self.name = name
        self.useStyleVersion = useStyleVersion
        self.expressionLocale = expressionLocale
        self.viewPagesAsTabs = viewPagesAsTabs
        self.element = element
        self.drillBehaviors = drillBehaviors
        self.queries = queries
        self.dataItems = dataItems
        self.pages = pages
        self.dataContainers = dataContainers

    def json(self):
        return {
            'CMID': self.CMID,
            'name': self.name,
            'xmlns' : self.xmlns, 
            'useStyleVersion' : self.useStyleVersion, 
            'expressionLocale' : self.expressionLocale, 
            'viewPagesAsTabs' : self.viewPagesAsTabs,
            'drillBehaviours': len(self.drillBehaviors),
            'queries': len(self.queries),
            'dataItems': len(self.dataItems),
            'pages': len(self.pages),
            'dataContainers': len(self.dataContainers)
        }

