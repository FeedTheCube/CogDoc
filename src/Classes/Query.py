class Query(object):
    """description of class"""
    def __init__(self, name, source, sourceName, joins, dataItems, filters, slicers, element, report=None, sourceTables=None):
        self.report = report
        self.name = name
        self.source = source
        self.sourceName = sourceName
        self.joins = joins
        self.sourceTables = sourceTables
        self.dataItems = dataItems
        self.filters = filters
        self.slicers = slicers
        self.element = element

    def json(self):
        return {
            'Report':self.report,
            'Name': self.name,
            'Source': self.source,
            'Source Name': self.sourceName,
            'Joins': self.joins,
            'Source Tables': self.sourceTables,
            'Data Items': len( self.dataItems ),
            'Filters': len(self.filters),
            'Slicers': self.slicers,
            }

