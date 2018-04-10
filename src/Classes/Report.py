class Report(object):
    """description of class"""

    author = ""
    defaultOutput = "" #xls, csv, pdf
    lastModified = "" 

    queries = []
    dataItems = []
    
    #ADD - schedule
    #ADD - saved outputs

    def __init__(self, CMID, storeID, name, xmlns, useStyleVersion, expressionLocale,  element, modelPath, viewPagesAsTabs=None, drillBehaviors = [], queries=[], dataItems=[], pages=[], dataContainers=[]):
        self.CMID = CMID
        self.storeID = storeID
        self.xmlns = xmlns
        self.name = name
        self.useStyleVersion = useStyleVersion
        self.expressionLocale = expressionLocale
        self.viewPagesAsTabs = viewPagesAsTabs
        self.element = element
        self.modelPath = modelPath
        self.drillBehaviors = drillBehaviors
        self.queries = queries
        self.dataItems = dataItems
        self.pages = pages
        self.dataContainers = dataContainers

    def json(self):
        return {
            'CMID': self.CMID,
            'Store ID': self.storeID,
            'Name': self.name,
            'xmlns' : self.xmlns, 
            'Use Style Version' : self.useStyleVersion,
            'Expression Locale' : self.expressionLocale,
            'View Pages As Tabs' : self.viewPagesAsTabs,
            'Model Path': self.modelPath,
            'Drill Behaviours': len(self.drillBehaviors),
            'Queries': len(self.queries),
            'Data Items': len(self.dataItems),
            'Pages': len(self.pages),
            'Data Containers': len(self.dataContainers)
        }

