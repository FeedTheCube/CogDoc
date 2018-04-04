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
            'Name': self.name,
            'xmlns' : self.xmlns, 
            'Use Style Version' : self.useStyleVersion,
            'Expression Locale' : self.expressionLocale,
            'View Pages As Tabs' : self.viewPagesAsTabs,
            'Drill Behaviours': len(self.drillBehaviors),
            'Queries': len(self.queries),
            'Data Items': len(self.dataItems),
            'Pages': len(self.pages),
            'Data Containers': len(self.dataContainers)
        }

