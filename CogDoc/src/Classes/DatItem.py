class DatItem(object):
    """description of class"""
    def __init__(self, _name, _aggregate, _rollupAggregate, _sort, _expression, _element):
        self.name = _name
        self.aggregate = _aggregate
        self.rollupAggregate = _rollupAggregate
        self.sort = _sort
        self.expression = _expression
        self.element = _element

    @classmethod
    def getDataItems(cls, element, namespace):
        dataItems = []
        dItemsIter = element.iter(namespace+"dataItem")
        for dataItem in dItemsIter:
            dI = DatItem(
                _name = dataItem.get("name"),
                _aggregate = dataItem.get("aggregate"),
                _rollupAggregate = dataItem.get("rollupAggregate"),
                _sort = dataItem.get("sort"),
                _expression = dataItem[0].text,
                _element = dataItem
                )
            dataItems.append(dI)
        return dataItems

    def JSON(self):
        return {
            'name': self.name,
            'aggregate': self.aggregate,
            'rollupAggregate': self.rollupAggregate,
            'sort': self.sort,
            'expression': self.expression
            }