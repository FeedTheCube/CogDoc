import src.Query.DataItem.DataItem

class Query(object):
    """description of class"""
    def __init__(self, _name, _source, _joins, _dataItems, _filters, _slicers):
        self.name = _name
        self.source = _source
        self.joins = _joins
        self.dataItems = _dataItems
        self.filters = _filters
        self.slicers = _slicers

    def getQueries(xmlSpec, namespace):
        print("retreiving queries")
        queries = xmlSpec.iter(namespace + "query")
        for query in queries:
            if query[0][0].tag == namespace+"queryRef":
                source = query[0][0].get("refQuery")
            if query[0][0].tag == namespace+"model":
                source = "model"
            qry = Query(
                    _name = query.get("name"),
                    _source = source,
                    _joins = None,
                    _dataItems = None,
                    #getDataItems,
                    _filters = None,
                    _slicers = None
                )
            print(
                "QueryName: ", qry.name, 
                ", Source: ", qry.source
                )
            #dataItems=getDataItems(query)
            #for item in dataItems:
            #    print("  "+ item.name, etree.tostring( item.element ))