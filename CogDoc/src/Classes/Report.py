class Report(object):
    """description of class"""

    author = ""
    defaultOutput = "" #xls, csv, pdf
    lastModified = "" 

    queries = []
    
    #ADD - schedule
    #ADD - saved outputs

    def __init__(self, name, _xmlns, _useStyleVersion, _expressionLocale, _viewPagesAsTabs, element, drillBehaviors = [], queries=[], dataItems=[], pages=[], dataContainers=[]):
        self.xmlns = _xmlns
        self.name = name
        self.useStyleVersion = _useStyleVersion
        self.expressionLocale = _expressionLocale
        self.viewPagesAsTabs = _viewPagesAsTabs
        self.element = element
        self.drillBehaviors = drillBehaviors
        self.queries = queries
        self.dataItems = dataItems
        self.pages = pages
        self.dataContainers = dataContainers

    def json(self):
        return {
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