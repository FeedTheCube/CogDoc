class Query(object):
    """description of class"""
    def __init__(self, name, source, joins, dataItems, filters, slicers, element, report=None):
        self.report = report
        self.name = name
        self.source = source
        self.joins = joins
        self.dataItems = dataItems
        self.filters = filters
        self.slicers = slicers
        self.element = element

    def json(self):
        return {
            'Report':self.report,
            'Name': self.name,
            'Source': self.source,
            'Joins': self.joins,
            'Data Items': len( self.dataItems ),
            'Filters': len(self.filters),
            'Slicers': self.slicers,
            }