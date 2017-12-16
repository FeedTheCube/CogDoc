class DataItem(object):
    """description of class"""
    def __init__(self, _name, _aggregate, _rollupAggregate, _sort, _expression, _element):
        self.name = _name
        self.aggregate = _aggregate
        self.rollupAggregate = _rollupAggregate
        self.sort = _sort
        self.expression = _expression
        self.element = _element

    def getDataItems(element, namespace):
        dataItems = []
        dItemsIter = element.iter(namespace+"dataItem")
        for dataItem in dItemsIter:
            dI = DataItem(
                _name = dataItem.get("name"),
                _aggregate = dataItem.get("aggregate"),
                _rollupAggregate = dataItem.get("rollupAggregate"),
                _sort = dataItem.get("sort"),
                _expression = dataItem[0].text,
                _element = dataItem
                )
            dataItems.append(dI)
         
        return dataItems
